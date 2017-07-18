import django_tables2 as tables
from bootcamp.medications.models import MedicationTime

class MedicationTable(tables.Table):

	
    class Meta:
    	model = MedicationTime