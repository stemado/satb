
from django import forms
from django.utils.translation import gettext_lazy as _
from careplus.medications.models import Medication, MedicationCompletion, MedicationTime
from extra_views import InlineFormSet
from django.forms import ModelForm
from datetime import datetime


class MedicationForm(forms.ModelForm):

    class Meta:
        model = Medication
        fields = ['medicationName', 'medicationDosage', 'medicationFrequency', 'medicationStartDate', 'medicationDistribution',  'medicationTimeSchedule', 'medicationTimeSchedule2', 'medicationTimeSchedule3', 'medicationTimeSchedule4', 'medicationTimeSchedule5', 'medicationTimeSchedule6',  'medicationQuantity', 'medicationType', 'medicationDiscontinuedStatus', 'medicationComment', 'medicationResident']


# class StatusForm(forms.ModelForm):

#     class Meta:
#         model = MedicationCompletion
#         fields = ['completionStatus', 'completionStatus2', 'completionNote', 'completionMedication']

class StatusForm(forms.ModelForm):

    class Meta:
        model = MedicationCompletion
        fields = ['completionStatus', 'completionNote', 'completionMedication']

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
