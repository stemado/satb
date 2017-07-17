
from django import forms
from django.utils.translation import gettext_lazy as _
from bootcamp.medications.models import Medication, MedicationCompletion, MedicationTime
from extra_views import InlineFormSet
from django.forms import ModelForm
from datetime import datetime


class MedicationForm(forms.ModelForm):

    # medicationName = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control'}),
    #     max_length=50)
    # medicationDosage = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control'}),
    #     max_length=50)
    # medicationFrequency = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control'}),
    #     max_length=50)
    # medicationTimeSchedule = forms.CharField(
    #     widget=forms.TimeInput(attrs={'class': 'form-control'}),
    #     )
    # medicationTimeSchedule2 = forms.CharField(
    #     widget=forms.TimeInput(attrs={'class': 'form-control'}),
    #     )
    # medicationTimeSchedule3 = forms.CharField(
    #     widget=forms.TimeInput(attrs={'class': 'form-control'}),
    #     )
    # medicationTimeSchedule4 = forms.CharField(
    #     widget=forms.TimeInput(attrs={'class': 'form-control'}),
    #     )
    # medicationTimeSchedule5 = forms.CharField(
    #     widget=forms.TimeInput(attrs={'class': 'form-control'}),
    #     )
    # medicationTimeSchedule6 = forms.CharField(
    #     widget=forms.TimeInput(attrs={'class': 'form-control'}),
    #     )
    # medicationTimeSchedule7 = forms.CharField(
    #     widget=forms.TimeInput(attrs={'class': 'form-control'}),
    #     )
    # medicationTimeSchedule8 = forms.CharField(
    #     widget=forms.TimeInput(attrs={'class': 'form-control'}),
    #     )
    # medicationTimeSchedule9 = forms.CharField(
    #     widget=forms.TimeInput(attrs={'class': 'form-control'}),
    #     )
    # medicationTimeSchedule10 = forms.CharField(
    #     widget=forms.TimeInput(attrs={'class': 'form-control'}),
    #     )
    # medicationTimeSchedule11 = forms.CharField(
    #     widget=forms.TimeInput(attrs={'class': 'form-control'}),
    #     )
    # medicationTimeSchedule12 = forms.CharField(
    #     widget=forms.TimeInput(attrs={'class': 'form-control'}),
    #     )
    # medicationTimeSchedule24 = forms.CharField(
    #     widget=forms.TimeInput(attrs={'class': 'form-control'}),
    #     )
    # medicationDistribution = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control'}),
    #     max_length=50)
    # medicationQuantity = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control'}),
    #     max_length=50)
    # medicationType = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control'}),
    #     max_length=50)
    # medicationComment = forms.CharField(
    #     widget=forms.Textarea(attrs={'class': 'form-control'}),
    #     max_length=500)





    class Meta:
        model = Medication
        fields = ['medicationResident', 'medicationName', 'medicationDosage', 'medicationFrequency', 'medicationStartDate', 'medicationDistribution',  'medicationTimeSchedule', 'medicationTimeSchedule2', 'medicationTimeSchedule3', 'medicationTimeSchedule4', 'medicationTimeSchedule5', 'medicationTimeSchedule6',  'medicationQuantity', 'medicationType', 'medicationDiscontinuedStatus', 'medicationComment']


# class StatusForm(forms.ModelForm):

#     class Meta:
#         model = MedicationCompletion
#         fields = ['completionStatus', 'completionStatus2', 'completionNote', 'completionMedication']

class StatusForm(forms.ModelForm):

    class Meta:
        model = MedicationCompletion
        fields = ['completionMedication', 'completionStatus', 'completionNote']

class MedicationStatusForm(forms.ModelForm):

    medicationName = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50)

    medicationComment = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        max_length=500)



class StatusFormSet(InlineFormSet):
    model = MedicationCompletion
    max_num = 1
