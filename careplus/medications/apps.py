from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class MedicationsConfig(AppConfig):
    name = 'careplus.medications'
    verbose_name = _('medications')

    def ready(self):

        import careplus.medications.signals  # noqa