

# Create your models here.

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import UpdateView

import bleach
from bootcamp.activities.models import Activity
from bootcamp.residents.models import Resident

@python_2_unicode_compatible
class PhysicianOrder(models.Model):
    orderMedication = models.CharField(default="John", max_length=50, null=True, blank=True)
    orderDetails = models.CharField(default="Doe", max_length=50, null=True, blank=True)
    orderTime = models.CharField(default="123456789", max_length=50, null=True, blank=True)
    orderPhysician = models.CharField(default="3/5/1980", max_length=50, null=True, blank=True)
    orderDate = models.CharField(default="Dr.John Kellenberger", max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = _("PhysicianOrder")
        verbose_name_plural = _("PhysicianOrders")
        ordering = ("-orderDate",)
 
    def __str__(self):
        return self.orderMedication


    def get_orders():
        orders = PhysicianOrder.objects.all()
        return orders




