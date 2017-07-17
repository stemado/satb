
from django import forms

from bootcamp.residents.models import Resident, EmergencyContact
from django.utils.translation import ugettext_lazy as _


class ResidentForm(forms.ModelForm):
    # residentFirstName = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control'}),
    #     max_length=50)
    # residentLastName = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control'}),
    #     max_length=50)
    # residentSSN = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control'}),
    #     max_length=9)
    # residentDOB = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control'}),
    #     max_length=10)
    # residentPrimaryPhysician = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control'}),
    #     max_length=50)
    # location = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control'}),
    #     max_length=15)
    # medicareNumber = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control'}),
    #     max_length=15)
    # dnr_status = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control'}),
    #     max_length=15)
    

    class Meta:
        model = Resident
        fields = ['residentFirstName', 'residentLastName', 'residentProfile', 'residentSSN', 'residentDOB', 'residentPrimaryPhysician', 'location', 'medicareNumber', 'dnr_status']


class EmergencyContactForm(forms.ModelForm):
    emergencyContactFirstName = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50)
    emergencyContactLastName = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50)
    emergencyContactRelationship = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=9)
    emergencyContactPhoneNumber = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=10)
    resident = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50)
    

    class Meta:
        model = EmergencyContact
        fields = ['emergencyContactFirstName', 'emergencyContactLastName', 'emergencyContactRelationship', 'emergencyContactPhoneNumber', 'resident']
