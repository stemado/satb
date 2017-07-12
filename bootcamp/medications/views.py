from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string


import markdown
from bootcamp.medications.forms import MedicationForm, StatusForm, MedicationStatusForm, StatusFormSet
from bootcamp.medications.models import Medication, MedicationCompletion, TimeMedicationOne
from bootcamp.decorators import ajax_required
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetView
import csv
from reportlab.pdfgen import canvas
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
    active_medications = Medication.get_active_medications()
    overdue_medications = Medication.get_overdue_medications()
    overdue_medications2 = Medication.get_overdue_medications2()
    return render(request, 'medications/all_medications.html', {'medications': medications,
        'active_medications': active_medications, 'overdue_medications': overdue_medications})

@login_required
def overdue_medications(request):
    medications = Medication.get_medications()
    active_medications = Medication.get_active_medications()
    overdue_medications = Medication.get_overdue_medications()
    overdue_medications2 = Medication.get_overdue_medications2()
    return render(request, 'medications/overdue_medications.html', {'medications': medications,
        'active_medications': active_medications, 'overdue_medications': overdue_medications, 'overdue_medications2': overdue_medications2})


@login_required
def active_medications(request):
    medications = Medication.get_medications()
    active_medications = Medication.get_active_medications()
    overdue_medications = Medication.get_overdue_medications()
    return render(request, 'medications/active_medications.html', {'medications': medications,
        'active_medications': active_medications, 'overdue_medications': overdue_medications})


#Check here to see if this view is correct.
@login_required
def medication(request, id):
    medication = get_object_or_404(Medication, id=id)
    return render(request, 'medications/medication.html', {'medication': medication})


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
def acceptRefuse(request, medication_id):

    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            status = form.save()
            status.save()

            return redirect('/medications/')
    else:
        form = StatusForm(initial={'completionMedication': medication_id})
    return render(request, 'medications/medication_status.html/', {'form': form})



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

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response
