from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class MedicationsConfig(AppConfig):
    name = 'bootcamp.medications'
    verbose_name = _('medications')

    def ready(self):

        import bootcamp.medications.signals  # noqa