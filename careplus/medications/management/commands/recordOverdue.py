from django.core.management.base import BaseCommand, CommandError
from careplus.medications.models import Medication, MedicationTime
from datetime import datetime
from datetime import timedelta

class Command(BaseCommand):
	help = 'Resets the medication status delivery to False at 12:00:01 AM'

	def handle(self, *args, **options):

		now = datetime.now()
		hourAfter = now - timedelta(hours=1, minutes=1)
		medication = MedicationCompletion.objects.filter(timeGivenStatus='False', timeDue__lte=hourAfter)
		if medication == True:
			MedicationTime.objects.filter(completion='False', timeDue__lte=hourAfter).update(completionMissed='True')
