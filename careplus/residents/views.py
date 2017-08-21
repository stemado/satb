from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

from datetime import datetime
import markdown
from careplus.residents.forms import ResidentForm, EmergencyContactForm
from careplus.residents.models import Resident, EmergencyContact
from careplus.medications.models import Medication, MedicationTime, MedicationCompletion

from careplus.decorators import ajax_required

def _residents(request, residents):
	return render(request, 'residents/residents.html', {
		'residents': residents
		})


@login_required
def residents(request):
	all_residents = Resident.get_residents()
	return _residents(request, all_residents)

#Check here to see if this view is correct.
@login_required
def resident(request, id):
    resident = get_object_or_404(Resident, id=id)
    medications = Medication.objects.filter(medicationResident_id=id)
    a = Medication.objects.filter(medicationResident_id=id).values_list('id', flat=True)
    overdue = MedicationTime.get_overdue_medications().filter(timeMedication_id__in=a)
    active = MedicationTime.get_active_medications().filter(timeMedication_id__in=a)
    prn = MedicationTime.objects.filter(timeMedication_id__in=a, timePRN=True)
    paginator = Paginator(medications, 10)
    page = request.GET.get('page')
    try:
        meds = paginator.page(page)
    except PageNotAnInteger:
        meds = paginator.page(1)
    except EmptyPage:
        meds = paginator.page(paginator.num_pages)
    return render(request, 'residents/resident.html', {'resident': resident, 'medications': medications, 'overdue': overdue, 'active': active, 'prn': prn, 'meds': meds})


@login_required
def create(request):
    if request.method == 'POST':
        form = ResidentForm(request.POST)
        if form.is_valid():
            resident = Resident()
            resident.residentFirstName = form.cleaned_data.get('residentFirstName')
            resident.residentLastName = form.cleaned_data.get('residentLastName')
            resident.residentSSN = form.cleaned_data.get('residentSSN')
            resident.residentDOB = form.cleaned_data.get('residentDOB')
            resident.residentPrimaryPhysician = form.cleaned_data.get('residentPrimaryPhysician')
            resident.location = form.cleaned_data.get('location')
            resident.medicareNumber = form.cleaned_data.get('medicareNumber')            
            resident.dnr_status = form.cleaned_data.get('dnr_status')
            resident.save()
            return redirect('/residents/')
    else:
        form = ResidentForm()
    return render(request, 'residents/create.html', {'form': form})


def edit(request, id):
    if id:
        resident = get_object_or_404(Resident, pk=id)
    else:
        resident = None

    if request.method == 'POST':
        form = ResidentForm(request.POST, instance=resident)
        if form.is_valid():
            form.save()
            return redirect('/residents/')
    else: 
        form = ResidentForm(instance=resident, initial={'residents': residents})
    return render(request, 'residents/edit.html', {'form': form})

@login_required
def rx_all(request, id):
    resident = Resident.objects.get(id=id)
    medications = Medication.objects.filter(medicationResident_id=id)
    active_medications = MedicationTime.get_active_medications()
    overdue_medications = MedicationTime.get_overdue_medications()
    prn = MedicationTime.get_prn_medications()
    paginator = Paginator(medications, 10)
    page = request.GET.get('page')
    try:
        meds = paginator.page(page)
    except PageNotAnInteger:
        meds = paginator.page(1)
    except EmptyPage:
        meds = paginator.page(paginator.num_pages)
    return render(request, 'residents/rx_all.html', {'meds': meds, 'medications': medications, 'prn': prn, 'resident': resident, 'active_medications': active_medications, 'overdue_medications': overdue_medications})

@login_required
def rx_overdue(request, id):
    resident = Resident.objects.get(id=id)
    medications = Medication.objects.filter(medicationResident_id=id)
    a = Medication.objects.filter(medicationResident_id=id).values_list('id', flat=True)
    overdue = MedicationTime.get_overdue_medications().filter(timeMedication_id__in=a)
    active_medications = MedicationTime.get_active_medications().filter(timeMedication_id__in=a)
    prn = MedicationTime.objects.filter(timeMedication_id__in=a, timePRN=True)
    return render(request, 'residents/rx_overdue.html', {'medications': medications,
        'active_medications': active_medications, 'prn': prn, 'resident': resident, 'overdue': overdue})


@login_required
def rx_active(request, id):
    resident = Resident.objects.get(id=id)
    medications = Medication.objects.filter(medicationResident_id=id)
    a = Medication.objects.filter(medicationResident_id=id).values_list('id', flat=True)
    active = MedicationTime.get_active_medications().filter(timeMedication_id__in=a)
    overdue_medications = MedicationTime.get_overdue_medications().filter(timeMedication_id__in=a)
    prn = MedicationTime.objects.filter(timeMedication_id__in=a, timePRN=True)
    return render(request, 'residents/rx_active.html', {'medications': medications,
        'active': active, 'resident': resident, 'prn': prn, 'overdue_medications': overdue_medications})


#NEED TO GET THE MEDICATION ID VARIABLE IN TO THE TIMEMEDICATION_ID OF PRN - HARD CODED MOMENTARILY
#UPDATE THE OTHER RX_ VIEWS TO CORRECT PRN VARIABLE
@login_required
def rx_prn(request, id):
    resident = Resident.objects.get(id=id)
    medications = Medication.objects.filter(medicationResident_id=id)
    a = Medication.objects.filter(medicationResident_id=id).values_list('id', flat=True)
    active = MedicationTime.get_active_medications().filter(timeMedication_id__in=a)
    overdue_medications = MedicationTime.get_overdue_medications().filter(timeMedication_id__in=a)
    prn = MedicationTime.objects.filter(timeMedication_id__in=a, timePRN=True)
    return render(request, 'residents/rx_prn.html', {'medications': medications,
        'active': active, 'resident': resident, 'prn': prn, 'overdue_medications': overdue_medications})

def medicationList(request, id):
    resident = Resident.objects.get(id=id)
    med = Medication.objects.filter(medicationResident_id=id, medicationDiscontinuedStatus = 'Active')

    return render(request, 'residents/med_list.html', {'med': med, 'resident': resident })

@login_required
def emergencycontact(request):
    if request.method == 'POST':
        form = EmergencyContactForm(request.POST)
        if form.is_valid():
            er = EmergencyContact()
            er.emergencyContactFirstName = form.cleaned_data.get('emergencyContactFirstName')
            er.emergencyContactLastName = form.cleaned_data.get('emergencyContactLastName')
            er.emergnecyContactRelationship = form.cleaned_data.get('emergnecyContactRelationship')
            er.emergencyContactPhoneNumber = form.cleaned_data.get('emergencyContactPhoneNumber')
            er.residentPrimaryPhysician = form.cleaned_data.get('residentPrimaryPhysician')
            er.resident = form.cleaned_data.get('resident')
            er.save()
            return redirect('/residents/')
    else:
        form = ResidentForm()
    return render(request, 'residents/create.html', {'form': form})

def deleteResident(request, id):
    article = get_object_or_404(Resident, pk=id).delete()

    return redirect ('/residents/')


