from django.core.management.base import BaseCommand, CommandError
from bootcamp.medications.models import Medication, MedicationTime

class Command(BaseCommand):
	help = 'Resets the medication status delivery to False at 12:00:01 AM'

	def handle(self, *args, **options):

		a = MedicationCompletion.objects.values('completionTime')
		b = MedicationTime.objects.filter(Q(timeDue__=a) | )

		now = datetime.now()
		hourAfter = now - timedelta(hours=1, minutes=1)
		medication = MedicationTime.objects.filter(timeGivenStatus='False', timeDue__lte=hourAfter)
		if medication == True:
			MedicationTime.objects.filter(timeGivenStatus='False', timeDue__lte=hourAfter).update(completionMissed='True')
