from datetime import timedelta
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
# import sendgrid
# import os
# from sendgrid.helpers.mail import *
from django.core.mail import send_mail
from django.contrib.auth.models import User
from careplus.medications.models import Medication, MedicationCompletion, MedicationTime
from careplus.residents.models import Resident


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


#Update the completiontime object with the parent timeDue for reporting
#purposes.
@receiver(post_save, sender=MedicationCompletion)
def f(sender, instance, created, **kwargs):

		a = instance.completionMedication_id
		b = MedicationTime.objects.filter(id=a).values_list('timeDue', flat=True)
		MedicationCompletion.objects.filter(id=instance.id).update(completionDue=b[0])



#Subtracts medication count each time medication given.
@receiver(post_save, sender=MedicationCompletion)	
def update_medication_count(sender, instance, created, **kwargs):	

	if created:
		a = instance.completionMedication_id
		b = MedicationTime.objects.filter(id=a).values('timeMedication_id')
		if instance.completionStatus == True:
			Medication.objects.filter(id=b).update(medicationQuantity=F('medicationQuantity') -1)


@receiver(post_save, sender=Medication, dispatch_uid='medication_time_add')
def create_medication_time(sender, instance, created, **kwargs):

	if created:
		time = timezone.now()
		a = instance.id
		b = instance.medicationTimeSchedule
		c = instance.medicationTimeSchedule2
		d = instance.medicationTimeSchedule3
		e = instance.medicationTimeSchedule4
		f = instance.medicationTimeSchedule5
		g = instance.medicationTimeSchedule6
		if instance.medicationTimeSchedule != None:
			MedicationTime.objects.create(timeStatus=None, timeGivenStatus=False, timeCreated=time, timeDue=b, timeMedication_id=a, timeGivenNote='Auto Generated')
		if instance.medicationTimeSchedule2 != None:
			MedicationTime.objects.create(timeStatus=None, timeGivenStatus=False, timeCreated=time, timeDue=c, timeMedication_id=a, timeGivenNote='Auto Generated')
		if instance.medicationTimeSchedule3 != None:
			MedicationTime.objects.create(timeStatus=None, timeGivenStatus=False, timeCreated=time, timeDue=d, timeMedication_id=a, timeGivenNote='Auto Generated')
		if instance.medicationTimeSchedule4 != None:
			MedicationTime.objects.create(timeStatus=None, timeGivenStatus=False, timeCreated=time, timeDue=e, timeMedication_id=a, timeGivenNote='Auto Generated')
		if instance.medicationTimeSchedule5 != None:
			MedicationTime.objects.create(timeStatus=None, timeGivenStatus=False, timeCreated=time, timeDue=f, timeMedication_id=a, timeGivenNote='Auto Generated')
		if instance.medicationTimeSchedule6 != None:
			MedicationTime.objects.create(timeStatus=None, timeGivenStatus=False, timeCreated=time, timeDue=g, timeMedication_id=a, timeGivenNote='Auto Generated')
		if instance.medicationDistribution == '0':
			MedicationTime.objects.create(timeStatus=None, timePRN=True, timeGivenStatus=None, timeCreated=time, timeDue=None, timeMedication_id=a, timeGivenNote='Auto Generated - PRN')



@receiver(post_save, sender=MedicationTime)
def create_medication_time_fill(sender, instance, created,  **kwargs):

	if created:
		med = Medication.objects.latest('medicationStartDate')
		a = med.medicationStartDate
		b = a.strftime('%d')
		c = int(b)
		time = timezone.now()
		d = instance.id
		if c > 1:
			while (c > 1):
				c = c - 1
				aa = a - timedelta(days=c)
				print("THIS IS FROM SIGNAL" + str(aa))
				fillRxTime = MedicationCompletion(completionStatus=None, completionDate=aa, completionDue=instance.timeDue, completionNote='SYSTEM RX PLACEHOLDER FILL', completionRx_id=med.id, completionMedication_id=instance.id)
				fillRxTime.save()

##########################################
###########Sendgrid Email Signals#########
##########################################

#Send Sendgrid Email - Demo/Test
# @receiver(post_save, sender=Resident)
# def send_resident_update(sender, instance, created, **kwargs):
# 	if created:
# 			email = 'stemado@outlook.com'
# 			subject = 'New Resident Added: ' + instance.residentFirstName + instance.residentLastName
# 			content = 'A new resident has added: ' + instance.residentFirstName
# 			send_mail(
# 				subject, 
# 				content, 
# 				'no-reply@careplus.com', 
# 				[email], 
# 				fail_silently=False
# 				)
# 			print('Email sent successfully!')


#Request Refill Signal - Needs some tweaking. 
# @receiver(post_save, sender=MedicationCompletion, dispatch_uid='medication_time_add')
# def request_medication_refill(sender, instance, created, **kwargs):

# 	med = Medication.objects.filter(id=instance.completionRx_id).values('medicationQuantity')
# 	count = int(med)
# 	if count[0] < 23:
# 			email = 'stemado@outlook.com'
# 			subject = 'Rx Refill Request: '
# 			content = 'Resident: E.g. John Doe/Medication ' + instance.completionRx
# 			send_mail(
# 				subject, 
# 				content, 
# 				'no-reply@careplus.com', 
# 				[email], 
# 				fail_silently=False
# 				)
# 			print('EMAIL SENT!')
# 	else:
# 		print('Count is at' + str(med))
