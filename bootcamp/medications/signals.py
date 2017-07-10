
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models import F
from django.dispatch import receiver

from bootcamp.medications.models import Medication, MedicationCompletion


#This reads when the MedicationComplation form is saved. 
#When saved, signal is sent and updates the medicationStatus to True. 
#Meaning this medication has had action taken on it.
@receiver(post_save, sender=MedicationCompletion)
def check_medication_status(sender, instance, created, **kwargs):


#1. Need to add an If statement for when completionStatus = False so medication object is not subtracted
	if created:
		a = instance.completionMedication_id
		b = Medication.objects.get(id=a)
		c = b.medicationStatus = 'True'
		b.save()


@receiver(post_save, sender=MedicationCompletion)
def update_medication_count(sender, instance, created, **kwargs):	

	if created:
		a = instance.completionMedication_id
		if instance.completionStatus == True:
			Medication.objects.filter(id=a).update(medicationQuantity=F('medicationQuantity') -1)





#2. Todo: Create new signal that utilizes update_or_created() to reduce number of queries to datbase. The above is quick and dirty solution to (A) Set medication status given to "True" and THEN subtract one from the medicationQuantity.




