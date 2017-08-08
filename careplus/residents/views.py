from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string


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
    medications = resident.medication_set.all()
    paginator = Paginator(medications, 10)
    page = request.GET.get('page')
    try:
        meds = paginator.page(page)
    except PageNotAnInteger:
        meds = paginator.page(1)
    except EmptyPage:
        meds = paginator.page(paginator.num_pages)
    return render(request, 'residents/resident.html', {'resident': resident, 'medications': medications, 'meds': meds})


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
    return render(request, 'residents/all_medications.html', {'meds': meds, 'medications': medications, 'active_medications': active_medications, 'overdue_medications': overdue_medications})

@login_required
def overdue_medications(request):
    medications = Medication.get_medications()
    overdue = MedicationTime.get_overdue_medications()
    active_medications = MedicationTime.get_active_medications()
    return render(request, 'residents/overdue_medications.html', {'medications': medications,
        'active_medications': active_medications, 'overdue': overdue})


@login_required
def active_medications(request):
    medications = Medication.get_medications()
    active = MedicationTime.get_active_medications()
    overdue_medications = MedicationTime.get_overdue_medications()
    return render(request, 'residents/active_medications.html', {'medications': medications,
        'active': active, 'overdue_medications': overdue_medications})


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


