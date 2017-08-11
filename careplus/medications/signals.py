from datetime import timedelta
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

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



# @receiver(post_save, sender=Medication, dispatch_uid='medication_time_add_2')
# def create_medication_time2(sender, instance, created, **kwargs):

# 	if created:
# 		time = timezone.now()
# 		a = instance.id
# 		b = instance.medicationTimeSchedule2
# 		if instance.medicationTimeSchedule2 != None:
# 			MedicationTime.objects.create(timeStatus=None, timeGivenStatus=False, timeCreated=time, timeDue=b, timeMedication_id=a, timeGivenNote='Auto Generated')


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


# @receiver(post_save, sender=MedicationTime, dispatch_uid='timefix2')
# def create_medication_time_fill2(sender, instance, created, **kwargs):

# 	if created:
# 		x2 = instance.medicationStartDate
# 		y2 = x2.strftime('%d')
# 		z2 = int(y2)
# 		time2 = timezone.now()
# 		a2 = instance.id
# 		med_two = MedicationTime.objects.latest('timeCreated')
# 		if z2 > 1:
# 			while (z2 > 1):
# 				z2 = z2 - 1
# 				ab = x2 - timedelta(days=z2)
# 				fill2 = MedicationCompletion.objects.create(completionStatus=None, completionDate=ab, completionDue=instance.medicationTimeSchedule2, completionNote='SYSTEM RX PLACEHOLDER FILL', completionRx_id=instance.id, completionMedication_id=med_two.id)
# 				fill2.save()
# 				print("completionDate" + str(ab))
# 				print("Med_One ID" + str(med_two.id))


# @receiver(post_save, sender=Medication)
# def create_medication_time3(sender, instance, created, **kwargs):

# 		time = timezone.now()
# 		a = instance.id
# 		b = instance.medicationTimeSchedule3
# 		if instance.medicationTimeSchedule3 != None:
# 			MedicationTime.objects.create(timeStatus=None, timeGivenStatus=False, timeDue=b, timeCreated=time, timeMedication_id=a, timeGivenNote='Auto Generated')

# @receiver(post_save, sender=Medication, dispatch_uid='timefix3')
# def create_medication_time_fill3(sender, instance, created, **kwargs):

# 	if created:
# 		x3 = instance.medicationStartDate
# 		y3 = x3.strftime('%d')
# 		z3 = int(y3)
# 		time3 = timezone.now()
# 		a3 = instance.id
# 		med_three = MedicationTime.objects.latest('timeCreated')
# 		if z3 > 1:
# 			while (z3 > 1):
# 				z3 = z3 - 1
# 				ac = x3 - timedelta(days=z3)
# 				MedicationCompletion.objects.create(completionStatus=None, completionDate=ac, completionDue=instance.medicationTimeSchedule3, completionNote='SYSTEM RX PLACEHOLDER FILL', completionRx_id=instance.id, completionMedication_id=med_three.id)
# 				print("completionDate" + str(ac))
# 				print("Med_One ID" + str(med_three.id))


# @receiver(post_save, sender=Medication)
# def create_medication_time4(sender, instance, created, **kwargs):

# 		time = timezone.now()
# 		a = instance.id
# 		b = instance.medicationTimeSchedule4
# 		if instance.medicationTimeSchedule4 != None:
# 			MedicationTime.objects.create(timeStatus=None, timeGivenStatus=False, timeDue=b, timeCreated=time,  timeMedication_id=a, timeGivenNote='Auto Generated')

# @receiver(post_save, sender=Medication)
# def create_medication_time_fill4(sender, instance, created, **kwargs):

# 	if created:
# 		x4 = instance.medicationStartDate
# 		y4 = x4.strftime('%d')
# 		z4 = int(y4)
# 		time4 = timezone.now()
# 		a4 = instance.id
# 		med_four = MedicationTime.objects.latest('timeCreated')
# 		try:
# 			while (z4 > 1):
# 				z4 = z4 - 1
# 				ad = x4 - timedelta(days=z4)
# 				MedicationCompletion.objects.create(completionStatus=None, completionDate=ad, completionDue=instance.medicationTimeSchedule4, completionNote='SYSTEM RX PLACEHOLDER FILL', completionRx_id=instance.id, completionMedication_id=med_four.id)
# 				print("completionDate" + str(ad))
# 				print("Med_One ID" + str(med_four.id))
# 		except:
# 			pass

# @receiver(post_save, sender=Medication)
# def create_medication_time5(sender, instance, created, **kwargs):

# 		time = timezone.now()
# 		a = instance.id
# 		b = instance.medicationTimeSchedule5
# 		if instance.medicationTimeSchedule5 != None:
# 			MedicationTime.objects.update_or_create(timeStatus=None, timeGivenStatus=False, timeDue=b, timeCreated=time,  timeMedication_id=a, timeGivenNote='Auto Generated')

# @receiver(post_save, sender=Medication)
# def create_medication_time_fill5(sender, instance, created, **kwargs):

# 	if created:
# 		x5 = instance.medicationStartDate
# 		y5 = x5.strftime('%d')
# 		z5 = int(y5)
# 		time5 = timezone.now()
# 		a5 = instance.id
# 		med_five = MedicationTime.objects.latest('timeCreated')
# 		try:
# 			while (z5 > 1):
# 				z5 = z5 - 1
# 				ae = x5 - timedelta(days=z5)
# 				MedicationCompletion.objects.create(completionStatus=None, completionDate=ae, completionDue=instance.medicationTimeSchedule5, completionNote='SYSTEM RX PLACEHOLDER FILL', completionRx_id=instance.id, completionMedication_id=med_five.id)
# 				print("completionDate" + str(ae))
# 				print("Med_One ID" + str(med_five.id))
# 		except:
# 			pass

# @receiver(post_save, sender=Medication)
# def create_medication_time6(sender, instance, created, **kwargs):

# 		time = timezone.now()
# 		a = instance.id
# 		b = instance.medicationTimeSchedule6
# 		if instance.medicationTimeSchedule6 != None:
# 			MedicationTime.objects.update_or_create(timeStatus=None, timeGivenStatus=False, timeDue=b, timeCreated=time,  timeMedication_id=a, timeGivenNote='Auto Generated')

# @receiver(post_save, sender=Medication)
# def create_medication_time_fill6(sender, instance, created, **kwargs):

# 	if created:
# 		x6 = instance.medicationStartDate
# 		y6 = x6.strftime('%d')
# 		z6 = int(y6)
# 		time6 = timezone.now()
# 		a6 = instance.id
# 		med_six = MedicationTime.objects.latest('timeCreated')
# 		try:
# 			while (z6 > 1):
# 				z6 = z6 - 1
# 				af = x6 - timedelta(days=z6)
# 				MedicationCompletion.objects.create(completionStatus=None, completionDate=af, completionDue=instance.medicationTimeSchedule6, completionNote='SYSTEM RX PLACEHOLDER FILL', completionRx_id=instance.id, completionMedication_id=med_five.id)
# 				print("completionDate" + str(af))
# 				print("Med_One ID" + str(med_six.id))
# 		except:
# 			pass
