
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models import F
from django.dispatch import receiver

from bootcamp.medications.models import Medication, MedicationCompletion, MedicationTime


#This reads when the MedicationComplation form is saved. 
#When saved, signal is sent and updates the medicationStatus to True. 
#Meaning this medication has had action taken on it.
@receiver(post_save, sender=MedicationCompletion)
def check_medication_status(sender, instance, created, **kwargs):

	if created:
		a = instance.completionMedication_id
		b = MedicationTime.objects.get(id=a)
		c = b.timeGivenStatus = 'True'
		b.save()


# @receiver(post_save, sender=MedicationCompletion)	
# def update_medication_count(sender, instance, created, **kwargs):	

# 	if created:
# 		if instance.completionStatus == True:
# 			Medication.objects.filter(id=b).update(medicationQuantity=F('medicationQuantity') -1)



@receiver(post_save, sender=Medication)
def create_medication_time(sender, instance, created, **kwargs):


#1. Need to add an If statement for when completionStatus = False so medication object is not subtracted
	if created:
		a = instance.id
		b = instance.medicationTimeSchedule
		c = instance.medicationTimeSchedule2
		if instance.medicationTimeSchedule != None:
			MedicationTime.objects.update_or_create(timeStatus=None, timeGivenStatus=False, timeDue=b, medication_id=a, timeGivenNote='Auto Generated')

@receiver(post_save, sender=Medication)
def create_medication_time2(sender, instance, created, **kwargs):


#1. Need to add an If statement for when completionStatus = False so medication object is not subtracted
	if created:
		a = instance.id
		b = instance.medicationTimeSchedule2
		if instance.medicationTimeSchedule2 != None:
			MedicationTime.objects.update_or_create(timeStatus=None, timeGivenStatus=False, timeDue=b, medication_id=a, timeGivenNote='Auto Generated')

#2. Todo: Create new signal that utilizes update_or_created() to reduce number of queries to datbase. The above is quick and dirty solution to (A) Set medication status given to "True" and THEN subtract one from the medicationQuantity.




