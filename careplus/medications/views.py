from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

import hashlib

import markdown
from careplus.medications.forms import MedicationForm, StatusForm, MedicationStatusForm, StatusFormSet
from careplus.residents.models import Resident
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
from django.db.models import Q
from datetime import datetime
from reportlab.lib.pagesizes import A4, cm 
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER 
from reportlab.lib import colors



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
    paginator = Paginator(medications, 2)
    page = request.GET.get('page')
    try:
        meds = paginator.page(page)
    except PageNotAnInteger:
        meds = paginator.page(1)
    except EmptyPage:
        meds = paginator.page(paginator.num_pages)
    return render(request, 'medications/all_medications.html', {'meds': meds, 'medications': medications, 'active_medications': active_medications, 'overdue_medications': overdue_medications})

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
    active = MedicationTime.get_active_medications()
    overdue_medications = MedicationTime.get_overdue_medications()
    return render(request, 'medications/active_medications.html', {'medications': medications,
        'active': active, 'overdue_medications': overdue_medications})


#Check here to see if this view is correct.
@login_required
def medication(request, id):
    medication = get_object_or_404(Medication, pk=id)
    time = MedicationTime.objects.filter(timeMedication=id)
    a = MedicationTime.objects.filter(timeMedication=id).values_list('id', flat=True)
    completion = MedicationCompletion.objects.filter(completionMedication__in=a).order_by('completionDate', 'completionDue')
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
def acceptRefuse(request, medication, rx):

    date = datetime.now().today()
    if request.method == 'POST':
        form = StatusForm(request.POST)
        # check = request.POST.get('csrf_token').encode('utf-8')
        # hashstring=hashlib.sha1(str(check)).hexdigest()
        # if request.session.get('sessionform') != hashstring:
        if form.is_valid():
            status = form.save()
            status.save()

            return redirect('/medications/')
    else:
        form = StatusForm(initial={'completionMedication': medication, 'completionRx': rx, 'completionDate': date })
    return render(request, 'medications/medication_status.html/', {'form': form})

# @login_required
# def pdfNewView(request):
#     medication = Medication.objects.filter(medicationResident_id=1)
#     time = MedicationTime.objects.filter(timeMedication_id=1)
#     a = MedicationTime.objects.filter(timeMedication_id=1).values_list('id', flat=True)
#     completion = MedicationCompletion.objects.filter(Q(completionMedication__in=a), Q(completionDate__gt='2017-6-30') & Q(completionDate__lt='2017-8-1')).order_by('-completionDue')
#     return render(request, 'medications/pdfview.html', {'medication': medication, 'time': time, 'completion': completion})

@login_required

def testpdf(request, id):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(letter))
    width, height = landscape(letter)
    # Start writing the PDF here
    p.drawString(100, 100, 'Hello world.')
    def coord(x, y, unit=1):
        x, y = x * unit, height - y * unit
        return x, y

##################################################
#Only part I am concerening myself with right now#
##################################################

    medication = Medication.objects.filter(medicationResident_id=id)
    data = []
    data.append(["Medication Name", "", "Hour", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"])

    for i in medication:
        row = []
        row.append(i.medicationName)
        row.append("")
        data.append(row)
        for j in MedicationTime.objects.filter(timeMedication=i.id):
            row.append(j.timeDue)
            row.append("AK")
        data.append(row)

  

    table = Table(data, colWidths=[100, 30, 50, 19] )
    table.setStyle(TableStyle([
        # ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ]))
    table.wrapOn(p, width, height)
    table.drawOn(p, *coord(.5, 9.6, cm))


    # End writing
    # p.grid([inch, 2*inch, 3*inch, 4*inch], [0.5*inch, inch, 1.5*inch, 2*inch, 2.5*inch])
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

@login_required
#Don't forget to add back 'time':, time to variables
def mar(request, mar_id):
    # resident = Resident.objects.get(id=1)
    # medication = resident.medication_set.all()
    # med = Medication.objects.filter()
    # test = Medication.completion_medication_set()
    medication = Medication.objects.filter(medicationResident_id=mar_id).order_by("medicationName", "id")
    # time = MedicationTime.objects.filter(Q(timeMedication_id=1) | Q(timeMedication_id=2) | Q(timeMedication_id=3)).order_by('id')
    resident = Resident.objects.filter(id=mar_id)[0]
    # rxcompletion = MedicationCompletion.objects.filter(Q(completionRx_id=1) | Q(completionRx_id=2), Q(completionDate__lt='2017-8-1') & Q(completionDate__gt='2017-6-30')).order_by('completionDate')
    paginator = Paginator(medication, 5)
    page = request.GET.get('page')
    try:
        meds = paginator.page(page)
    except PageNotAnInteger:
        meds = paginator.page(1)
    except EmptyPage:
        meds = paginator.page(paginator.num_pages)


    return render(request, 'medications/mar.html', {'medication': medication, 'resident': resident, 'meds': meds})

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


