from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string


import markdown
from bootcamp.residents.forms import ResidentForm, EmergencyContactForm
from bootcamp.residents.models import Resident, EmergencyContact
from bootcamp.decorators import ajax_required

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
    return render(request, 'residents/resident.html', {'resident': resident})


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


