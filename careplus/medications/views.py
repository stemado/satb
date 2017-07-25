from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string


import markdown
from careplus.medications.forms import MedicationForm, StatusForm, MedicationStatusForm, StatusFormSet
from careplus.medications.models import Medication, MedicationCompletion, MedicationTime
from careplus.decorators import ajax_required
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetView
import csv
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.platypus.tables import Table
cm = 2.54
from io import BytesIO
from django.dispatch import receiver
from django.db.models.signals import post_save



def _medications(request, medications):
	return render(request, 'medications/all_medications.html', {
		'medications': medications
		})


def _overdue_medications(request, medications):
    return render(request, 'medications/overdue_medications.html', {
        'medications': medications
        })

def _active_medications(request, medications):
    return render(request, 'medications/active_medications.html', {
        'medications': medications
        })



@login_required
def medications(request):
    medications = Medication.get_medications()
    active_medications = MedicationTime.get_active_medications()
    overdue_medications = MedicationTime.get_overdue_medications()
    paginator = Paginator(medications, 10)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'medications/all_medications.html', {'users': users, 'medications': medications, 'active_medications': active_medications, 'overdue_medications': overdue_medications})

@login_required
def overdue_medications(request):
    medications = Medication.get_medications()
    overdue = MedicationTime.get_overdue_medications()
    active_medications = MedicationTime.get_active_medications()
    return render(request, 'medications/overdue_medications.html', {'medications': medications,
        'active_medications': active_medications, 'overdue': overdue})


@login_required
def active_medications(request):
    medications = Medication.get_medications()
    active_medications = MedicationTime.get_active_medications()
    overdue_medications = MedicationTime.get_overdue_medications()
    return render(request, 'medications/active_medications.html', {'medications': medications,
        'active_medications': active_medications, 'overdue_medications': overdue_medications})


#Check here to see if this view is correct.
@login_required
def medication(request, id):
    medication = get_object_or_404(Medication, pk=id)
    time = MedicationTime.objects.filter(timeMedication=id)
    a = MedicationTime.objects.filter(timeMedication=id).values_list('id', flat=True)
    completion = MedicationCompletion.objects.filter(completionMedication__in=a)
    return render(request, 'medications/medication.html', {'medication': medication, 'time': time, 'completion': completion})


@login_required
def createMedication(request, resident_id):
    if request.method == 'POST':
        form = MedicationForm(request.POST)
        if form.is_valid():
            medication = form.save()
            medication.medicationName = form.cleaned_data.get('medicationName')
            medication.medicationDosage = form.cleaned_data.get('medicationDosage')
            medication.medicationFrequency = form.cleaned_data.get('medicationFrequency')
            medication.medicationDistribution = form.cleaned_data.get('medicationDistribution')
            medication.medicationQuantity = form.cleaned_data.get('medicationQuantity')
            medication.medicationType = form.cleaned_data.get('medicationType')
            medication.medicationStatus = form.cleaned_data.get('medicationStatus')
            medication.medicationComment = form.cleaned_data.get('medicationComment')
            medication.medicationSlug = form.cleaned_data.get('medicationSlug')
            medication.medicationTimeSchedule = form.cleaned_data.get('medicationTimeSchedule')
            medication.save()
            return redirect('activeMedications')
    else:
        form = MedicationForm(initial={'medicationResident': resident_id})
    return render(request, 'medications/create.html', {'form': form})



def editMedication(request, id):
    if id:
        medication = get_object_or_404(Medication, pk=id)
    else:
        medication = None

    if request.method == 'POST':
        form = MedicationForm(request.POST, instance=medication)
        if form.is_valid():
            form.save()
            return redirect('/medications/')
    else: 
        form = MedicationForm(instance=medication, initial={'medication': medication})
    return render(request, 'medications/edit.html', {'form': form})

@login_required
#THIS WILL HAVE TO BE UPDATED TO MAKE THIS A ONE TO MANY RELATIONSHIP, NOT WITH MEDICATIONS BUT ALL TIME SCHEDULE TABLES 
def acceptRefuse(request, medication):

    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            status = form.save()
            status.save()

            return redirect('/medications/')
    else:
        form = StatusForm(initial={'completionMedication': medication})
    return render(request, 'medications/medication_status.html/', {'form': form})

@login_required
def pdfNewView(request):
    medication  = Medication.objects.all()
    record = MedicationCompletion.objects.all()
    return render(request, 'medications/pdfview.html', {'medication': medication})



class EditMedicationUpdate(UpdateWithInlinesView):
    model = Medication
    inlines = [StatusFormSet, ]
    fields = ['medicationStatus']

    def post(self, request):
        return redirect ("testMedication")


def csv_view(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="testpdf.csv"'

    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C',  ' "Testing"', "Here's a quote"])

    return response

def pdf_view(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'

    elements = []

    doc = SimpleDocTemplate(response, rightMargin=0, leftMargin=6.5 * cm, topMargin=0.3 * cm, bottomMargin=0)

    data=[(1, 2, 3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31),(3,4,5,6),(5,6,7,8),(7,8,9,10)]
    table = Table(data, colWidths=18, rowHeights=20)
    elements.append(table)
    doc.build(elements) 

    return response



# def pdf_view(request):
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'

#     buffer = BytesIO()
#     p = canvas.Canvas(buffer)

#     # Start writing the PDF here
#     p.setLineWidth(.3)
#     p.setFont('Helvetica', 12)
 
#     p.drawString(30,750,'OFFICIAL COMMUNIQUE')
#     p.drawString(30,735,'OF ACME INDUSTRIES')
#     p.drawString(500,750,"12/12/2010")
#     p.line(480,747,580,747)
 
#     p.drawString(275,725,'AMOUNT OWED:')
#     p.rect(500,725,"$1,000.00")
#     p.line(378,723,580,723)
 
#     p.drawString(30,703,'RECEIVED BY:')
#     p.line(120,700,580,700)
#     p.drawString(120,703,"JOHN DOE")
#     p.drawString(100, 100, 'Hello world.')
#     # End writing

#     p.showPage()
#     p.save()

#     pdf = buffer.getvalue()
#     buffer.close()
#     response.write(pdf)

#     return response
