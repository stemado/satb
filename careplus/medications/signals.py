
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.db.models import F
from django.dispatch import receiver
from datetime import timedelta
from datetime import datetime

from careplus.medications.models import Medication, MedicationCompletion, MedicationTime

##This may need to go under each Signal for new record time, becuase the completion is for the record time not the medication. 


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


#Finally Works. Just need to get "<QuerySet:[TIME]> value out of it and just keep value. 
@receiver(post_save, sender=MedicationCompletion)
def f(sender, instance, created, **kwargs):

		a = instance.completionMedication_id
		b = MedicationTime.objects.filter(id=a).values_list('timeDue', flat=True)
		MedicationCompletion.objects.filter(id=instance.id).update(completionDue=b[0])




@receiver(post_save, sender=MedicationCompletion)	
def update_medication_count(sender, instance, created, **kwargs):	

	if created:
		a = instance.completionMedication_id
		b = MedicationTime.objects.filter(id=a).values('timeMedication_id')
		if instance.completionStatus == True:
			Medication.objects.filter(id=b).update(medicationQuantity=F('medicationQuantity') -1)



@receiver(post_save, sender=Medication)
def create_medication_time(sender, instance, created, **kwargs):
		time = datetime.now()
		a = instance.id
		b = instance.medicationTimeSchedule
		c = instance.medicationTimeSchedule2
		d = instance.medicationTimeSchedule3
		e = instance.medicationTimeSchedule4
		f = instance.medicationTimeSchedule5
		g = instance.medicationTimeSchedule6
		x = instance.medicationStartDate
		y = x.strftime('%d')
		z = int(y)

		if instance.medicationTimeSchedule != None:
			MedicationTime.objects.update_or_create(timeStatus=None, timeGivenStatus=False, timeDue=b, timeCreated=time, timeMedication_id=a, timeGivenNote='Auto Generated')
			med_one = MedicationTime.objects.latest('timeCreated')
			print(med_one.id)
			if z > 1:
				while (z > 0):
					z = z - 1
					nd = x - timedelta(days=z)
					MedicationCompletion.objects.create(completionStatus=None, completionDate=nd, completionDue=instance.medicationTimeSchedule, completionRx_id=instance.id, completionMedication_id=med_one.id)
					print(nd)
		if instance.medicationTimeSchedule2 != None:
			MedicationTime.objects.update_or_create(timeStatus=None, timeGivenStatus=False, timeDue=c, timeCreated=time, timeMedication_id=a, timeGivenNote='Auto Generated')
			med_two = MedicationTime.objects.latest('timeCreated')
			print(med_two.id)
			if z > 1:
				while (z > 1):
					z = z - 1
					nd = x - timedelta(days=z)
					MedicationCompletion.objects.create(completionStatus=None, completionDate=nd, completionDue=instance.medicationTimeSchedule2, completionRx_id=instance.id, completionMedication_id=med_two.id)
		if instance.medicationTimeSchedule3 != None:
			MedicationTime.objects.update_or_create(timeStatus=None, timeGivenStatus=False, timeDue=d, timeMedication_id=a, timeCreated=time, timeGivenNote='Auto Generated')
			med_three = MedicationTime.objects.latest('timeCreated')
			print(med_three.id)
			if z > 1:
				while (z > 1):
					z = z - 1
					nd = x - timedelta(days=z)
					MedicationCompletion.objects.create(completionStatus=None, completionDate=nd, completionDue=instance.medicationTimeSchedule3, completionRx_id=instance.id, completionMedication_id=med_three.id)
		if instance.medicationTimeSchedule4 != None:
			MedicationTime.objects.update_or_create(timeStatus=None, timeGivenStatus=False, timeDue=e, timeMedication_id=a, timeCreated=time, timeGivenNote='Auto Generated')
			med_four = MedicationTime.objects.latest('timeCreated')
			print(med_four.id)
			if z > 1:
				while (z > 1):
					z = z - 1
					nd = x - timedelta(days=z)
					MedicationCompletion.objects.create(completionStatus=None, completionDate=nd, completionDue=instance.medicationTimeSchedule4, completionRx_id=instance.id, completionMedication_id=med_four.id)
		if instance.medicationTimeSchedule5 != None:
			MedicationTime.objects.update_or_create(timeStatus=None, timeGivenStatus=False, timeDue=f, timeMedication_id=a, timeCreated=time, timeGivenNote='Auto Generated')
			med_five = MedicationTime.objects.latest('timeCreated')
			print(med_five.id)
			if z > 1:
				while (z > 1):
					z = z - 1
					nd = x - timedelta(days=z)
					MedicationCompletion.objects.create(completionStatus=None, completionDate=nd, completionDue=instance.medicationTimeSchedule5, completionRx_id=instance.id, completionMedication_id=med_five.id)
		if instance.medicationTimeSchedule6 != None:
			MedicationTime.objects.update_or_create(timeStatus=None, timeGivenStatus=False, timeDue=g, timeMedication_id=a, timeCreated=time, timeGivenNote='Auto Generated')
			med_six = MedicationTime.objects.latest('timeCreated')
			print(med_six.id)
			if z > 1:
				while (z > 1):
					z = z - 1
					nd = x - timedelta(days=z)
					MedicationCompletion.objects.create(completionStatus=None, completionDate=nd, completionDue=instance.medicationTimeSchedule6, completionRx_id=instance.id, completionMedication_id=med_six.id)

# @receiver(post_save, sender=Medication)
# def complete_mar_month(sender, instance, created, **kwargs):
# 	if created:
# 		
# 		w = MedicationTime.objects.latest('timeCreated')
# 			print(w.id)
# 			if z > 1:
# 				while (z > 0):
# 					z = z - 1
# 					nd = x - timedelta(days=z)
# 					if instance.medicationTimeSchedule != None:
# 						MedicationCompletion.objects.create(completionStatus=None, completionDate=nd, completionDue=instance.medicationTimeSchedule, completionRx_id=instance.id, completionMedication_id=w.id)
# 					if instance.medicationTimeSchedule2 != None:
# 						MedicationCompletion.objects.create(completionStatus=None, completionDate=nd, completionDue=instance.medicationTimeSchedule2, completionRx_id=instance.id, completionMedication_id=w.id)
# 					if instance.medicationTimeSchedule3 != None:
# 						MedicationCompletion.objects.create(completionStatus=None, completionDate=nd, completionDue=instance.medicationTimeSchedule3, completionRx_id=instance.id, completionMedication_id=w.id)
# 					if instance.medicationTimeSchedule4 != None:
# 						MedicationCompletion.objects.create(completionStatus=None, completionDate=nd, completionDue=instance.medicationTimeSchedule4, completionRx_id=instance.id, completionMedication_id=w.id)
# 					if instance.medicationTimeSchedule5 != None:
# 						MedicationCompletion.objects.create(completionStatus=None, completionDate=nd, completionDue=instance.medicationTimeSchedule5, completionRx_id=instance.id, completionMedication_id=w.id)
# 					if instance.medicationTimeSchedule6 != None:
# 						MedicationCompletion.objects.create(completionStatus=None, completionDate=nd, completionDue=instance.medicationTimeSchedule6, completionRx_id=instance.id, completionMedication_id=w.id)



# @receiver(post_save, sender=Medication)
# def create_medication_time2(sender, instance, created, **kwargs):


# #1. Need to add an If statement for when completionStatus = False so medication object is not subtracted

# 		a = instance.id
# 		b = instance.medicationTimeSchedule2
# 		if instance.medicationTimeSchedule2 != None:
# 			MedicationTime.objects.update_or_create(timeStatus=None, timeGivenStatus=False, timeDue=b, timeMedication_id=a, timeGivenNote='Auto Generated')

# @receiver(post_save, sender=Medication)
# def create_medication_time3(sender, instance, created, **kwargs):


# #1. Need to add an If statement for when completionStatus = False so medication object is not subtracted

# 		a = instance.id
# 		b = instance.medicationTimeSchedule3
# 		if instance.medicationTimeSchedule3 != None:
# 			MedicationTime.objects.update_or_create(timeStatus=None, timeGivenStatus=False, timeDue=b, timeMedication_id=a, timeGivenNote='Auto Generated')

# @receiver(post_save, sender=Medication)
# def create_medication_time4(sender, instance, created, **kwargs):


# #1. Need to add an If statement for when completionStatus = False so medication object is not subtracted

# 		a = instance.id
# 		b = instance.medicationTimeSchedule4
# 		if instance.medicationTimeSchedule4 != None:
# 			MedicationTime.objects.update_or_create(timeStatus=None, timeGivenStatus=False, timeDue=b, timeMedication_id=a, timeGivenNote='Auto Generated')

# @receiver(post_save, sender=Medication)
# def create_medication_time5(sender, instance, created, **kwargs):


# #1. Need to add an If statement for when completionStatus = False so medication object is not subtracted
# 	if created:
# 		a = instance.id
# 		b = instance.medicationTimeSchedule5
# 		if instance.medicationTimeSchedule5 != None:
# 			MedicationTime.objects.update_or_create(timeStatus=None, timeGivenStatus=False, timeDue=b, timeMedication_id=a, timeGivenNote='Auto Generated')

# @receiver(post_save, sender=Medication)
# def create_medication_time6(sender, instance, created, **kwargs):

# #1. Need to add an If statement for when completionStatus = False so medication object is not subtracted
# 	if created:
# 		a = instance.id
# 		b = instance.medicationTimeSchedule6
# 		if instance.medicationTimeSchedule6 != None:
# 			MedicationTime.objects.update_or_create(timeStatus=None, timeGivenStatus=False, timeDue=b, timeMedication_id=a, timeGivenNote='Auto Generated')

# #2. Todo: Create new signal that utilizes update_or_created() to reduce number of queries to datbase. The above is quick and dirty solution to (A) Set medication status given to "True" and THEN subtract one from the medicationQuantity.




