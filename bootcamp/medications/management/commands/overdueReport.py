from django.core.management.base import BaseCommand, CommandError
from bootcamp.medications.models import Medication, MedicationTime, MedicationCompletion
from datetime import datetime

class Command(BaseCommand):
	help = 'Resets the medication status delivery to False at 12:00:01 AM'

	def handle(self, *args, **options):

		a = instance.completionMedication_id
		b = MedicationTime.objects.filter(id=a).values_list('timeDue', flat=True)
		c = MedicationCompletion.objects.filter(id=instance.id)
		instance.completionDue=b
		instance.save()