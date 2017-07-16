from django.core.management.base import BaseCommand, CommandError
from bootcamp.medications.models import Medication, MedicationTime

class Command(BaseCommand):
	help = 'Resets the medication status delivery to False at 12:00:01 AM'

	def handle(self, *args, **options):
		MedicationTime.objects.update(timeGivenStatus='False')