
from django import forms

from careplus.physicianorders.models import PhysicianOrder


class PhysicianOrderForm(forms.ModelForm):

    orderMedication = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50)
    orderDetails = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50)
    orderTime = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50)
    orderPhysician = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50)
    orderDate = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50)

    class Meta:
        model = PhysicianOrder
        fields = '__all__'

from django import forms

from careplus.physicianorders.models import PhysicianOrder


class PhysicianOrderForm(forms.ModelForm):

    orderMedication = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50)
    orderDetails = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50)
    orderTime = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50)
    orderPhysician = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50)
    orderDate = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50)

    class Meta:
        model = PhysicianOrder

        fields = ['orderMedication', 'orderDetails', 'orderTime', 'orderPhysician', 'orderDate']