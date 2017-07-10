from __future__ import unicode_literals
from django.dispatch import receiver
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import UpdateView
from django.template.defaultfilters import slugify
import bleach
from bootcamp.activities.models import Activity
from bootcamp.residents.models import Resident
from django_filters import ModelMultipleChoiceFilter
from django_filters import rest_framework as filters
from django.utils import timezone
from django.db.models import signals, Count, Q
from datetime import timedelta
from django.utils import timezone
from django.db.models import signals





class MedicationQuerySet(models.QuerySet):

    def medicationDeliveryTime(self):

        now = datetime.now()
        hourBefore = now - timedelta(hours=1)
        hourAfter = now + timedelta(hours=1)
        yesterday = now - timedelta(days=1)
        tomorrow = now + timedelta(days=1)


        return self.filter(medicationTimeSchedule__range=(hourBefore, hourAfter))

    def medicationDeliveryStatus(self):
        return self.filter(medicationStatus='False')

    def medicationDeliveryOverdue(self):

        now = datetime.now()
        hourAfter = now - timedelta(hours=1, minutes=1)
        currentDay = now - timedelta()

        return self.filter(Q(medicationRecordReset__lt=(now)) & Q(medicationTimeSchedule__lte=(hourAfter)))

class MedicationManager(models.Manager):
    def get_queryset(self):
        return MedicationQuerySet(self.model, using=self._db)

    def medicationDeliveryTime(self):
        return self.get_queryset().medicationDeliveryTime()

    def medicationDeliveryStatus(self):
        return self.get_queryset().medicationDeliveryStatus()

    def medicationDeliveryOverdue(self):
        return self.get_queryset().medicationDeliveryOverdue()

    def medicationReset(self):
        return self.get_queryset().medicationReset()

@python_2_unicode_compatible
class Medication(models.Model):

    STATUS_CHOICES = (('False', 'Not Given'), ('True', 'Given'))
    MISSED_CHOICES = (('False', 'False'), ('True', 'True'))
    DISCONTINUED_CHOICES = (('Active', 'Active'), ('Discontinued', 'Discontinued'))
    DISTRUBUTION_CHOICES = (('1', 'Every Day'), ('2', '2 times A Day'), ('3', '3 times a day'), ('4', '4 times a day'), ('5', '5 times a day'), ('6', '6 times a day'), ('7', '7 times a day'), ('8', '8 times a day'), ('9', '9 times a day'), ('10', '10 times a day'), ('11', '11 times a day'), ('12', '12 times a day'), ('24', '24 times a day'))

    medicationName = models.CharField(verbose_name="Medication Name", default="Medication", max_length=50, null=True, blank=True)
    medicationSlug = models.SlugField(verbose_name="Slug", max_length=255, null=True, blank=True)
    medicationDosage = models.CharField(verbose_name="Dosage", default="e.g. 120 mg", max_length=50, null=True, blank=True)
    medicationFrequency = models.CharField(verbose_name="Frequency", max_length=50, null=True, blank=True)
    medicationDistribution = models.CharField(verbose_name="Distribution", choices=DISTRUBUTION_CHOICES, max_length=50, null=True, blank=True)
    medicationQuantity = models.IntegerField(verbose_name="Quantity", default="30", null=True, blank=True)
    medicationType = models.CharField(verbose_name="Drug Type", default="Narcotic", max_length=20, null=True, blank=True)
    medicationStatus = models.CharField(verbose_name="Current Status", choices=STATUS_CHOICES, max_length=10, default=False)
    medicationComment = models.CharField(verbose_name="Physician Order|Notes?", max_length=500, null=True, blank=True)
    medicationStartDate = models.DateField(verbose_name="Medication Start Date", default=datetime.now, blank=True, null=True)
    medicationTimeSchedule = models.TimeField(verbose_name="Time 1", default=datetime.now, blank=True, null=True)
    medicationTimeSchedule2 = models.TimeField(verbose_name="Time 2", default=datetime.now, blank=True, null=True)
    medicationTimeSchedule3 = models.TimeField(verbose_name="Time 3", default=datetime.now, blank=True, null=True)
    medicationTimeSchedule4 = models.TimeField(verbose_name="Time 4", default=datetime.now, blank=True, null=True)
    medicationTimeSchedule5 = models.TimeField(verbose_name="Time 5", default=datetime.now, blank=True, null=True)
    medicationTimeSchedule6 = models.TimeField(verbose_name="Time 6", default=datetime.now, blank=True, null=True)
    medicationTimeSchedule7 = models.TimeField(verbose_name="Time 7", default=datetime.now, blank=True, null=True)
    medicationTimeSchedule8 = models.TimeField(verbose_name="Time 8", default=datetime.now, blank=True, null=True)
    medicationTimeSchedule9 = models.TimeField(verbose_name="Time 9", default=datetime.now, blank=True, null=True)
    medicationTimeSchedule10 = models.TimeField(verbose_name="Time 10", default=datetime.now, blank=True, null=True)
    medicationTimeSchedule11 = models.TimeField(verbose_name="Time 11", default=datetime.now, blank=True, null=True)
    medicationTimeSchedule12 = models.TimeField(verbose_name="Time 12", default=datetime.now, blank=True, null=True)
    medicationTimeSchedule24 = models.TimeField(verbose_name="(13-24)", default=datetime.now, blank=True, null=True)
    medicationDiscontinuedStatus = models.CharField(verbose_name="DC Status", choices=DISCONTINUED_CHOICES, max_length=15, default='Active', blank=True, null=True)
    medicationDateTimeAdded = models.DateTimeField(auto_now_add=True)
    medicationMissed = models.CharField(verbose_name="Medication Missed", choices=MISSED_CHOICES, max_length=12, default='False', blank=True, null=True)
    medicationRecordReset = models.DateTimeField(default=datetime.now, blank=True, null=True)
    medicationResident = models.ForeignKey('residents.Resident', on_delete=models.CASCADE, verbose_name="Resident Name")
    created_by_user = models.ForeignKey(User, null=True, blank=True, related_name="+" )
    
    objects = MedicationQuerySet.as_manager()

    class Meta:
        verbose_name = _("Medication")
        verbose_name_plural = _("Medications")
        ordering = ('-medicationName',)

  
   

    def __str__(self):
        return (self.medicationName)

    def get_medications():
        medications = Medication.objects.all().order_by('-medicationResident')
        return medications

    def get_overdue_medications():
        medication = Medication.objects.filter(medicationStatus=False).medicationDeliveryOverdue()
        return medication


    def get_active_medications():
        medication = Medication.objects.medicationDeliveryTime().medicationDeliveryStatus()
        return medication


    def get_medication(self):
        return Medication.objects.filter(medication=self)


    def get_status(self):
        return MedicationCompletion.objects.filter(completionMedication=self)



@python_2_unicode_compatible
class MedicationCompletion(models.Model):

    BOOL_CHOICES = ((True, 'Accepted'), (False, 'Refused'))
    MISSED_CHOICES = (('False', 'False'), ('True', 'True'))

    completionStatus = models.NullBooleanField(verbose_name="Current Status", choices=BOOL_CHOICES, default='')
    completionMissed = models.CharField(verbose_name="Medicaton Missed", choices=MISSED_CHOICES, default='False', max_length=12, null=True, blank=True)
    completionTime = models.TimeField(verbose_name="Time Given", auto_now_add=True)
    completionDate = models.DateField(verbose_name="Date Given", auto_now_add=True)
    completionNote = models.CharField(verbose_name="Note", max_length=500, null=True, blank=True)    
    completionMedication = models.ForeignKey(Medication, on_delete=models.CASCADE)


    def __str__(self):
        return (self.completionStatus)




 
