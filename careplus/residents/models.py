
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import UpdateView

import bleach
from careplus.activities.models import Activity

@python_2_unicode_compatible
class Resident(models.Model):

    GENDER = (('Male', 'Male'), ('Female', 'Female'))
    DNR_STATUS = (('Active', 'Active'), ('Inactive', 'Inactive'))

    residentFirstName = models.CharField("First Name", default="John", max_length=50, null=True, blank=True)
    residentLastName = models.CharField("Last Name", default="Doe", max_length=50, null=True, blank=True)
    residentSSN = models.CharField("SSN", default="123456789", max_length=50, null=True, blank=True)
    residentDOB = models.CharField("DOB", default="3/5/1980", max_length=50, null=True, blank=True)
    residentPrimaryPhysician = models.CharField("Primary Physician", default="Dr.John Kellenberger", max_length=50, null=True, blank=True)
    residentGender = models.CharField(verbose_name="Gender", choices=GENDER, max_length=30, null=True, blank=True)
    residentStatus = models.CharField(verbose_name="Status", choices=DNR_STATUS, max_length=30, null=True, blank=True)
    location = models.CharField( "Room", default="Room 8", max_length=50, null=True, blank=True)
    residentProfile = models.FileField(upload_to='media/resident_pictures/', null=True, blank=True)
    medicareNumber = models.CharField("Medicare Number", default="ZSY20193992", max_length=20, null=True)
    dnr_status = models.CharField("DNR Status", choices=DNR_STATUS, default='Active', max_length=50, null=True, blank=True)


    class Meta:
        verbose_name = _("Resident")
        verbose_name_plural = _("Residents")
        ordering = ("-residentLastName",)
 
    def __str__(self):
        return '%s %s' % (self.residentFirstName, self.residentLastName)

    def get_picture(self):
        no_picture = 'http://trybootcamp.vitorfs.com/static/img/user.png'
        try:
            filename = settings.MEDIA_ROOT + '/resident_pictures/' +\
                self.resident + '.jpg'
            picture_url = settings.MEDIA_URL + 'resident_pictures/' +\
                self.resident + '.jpg'
            if os.path.isfile(filename):
                return picture_url
            else:
                gravatar_url = 'http://trybootcamp.vitorfs.com/static/img/user.png'
                return gravatar_url

        except Exception:
            return no_picture

    def get_residents():
        residents = Resident.objects.all()
        return residents

    def get_medications():
        medications = Resident.medication_set.all()
        return medications


    def get_contact(self):
        return EmergencyContact.objects.filter(resident=self)

    def get_resident_photo(self):
        no_picture = 'http://trybootcamp.vitorfs.com/static/img/user.png'
        try:
            filename = settings.MEDIA_ROOT + '/resident_pictures/' +\
                self.user.username + '.jpg'
            picture_url = settings.MEDIA_URL + 'profile_pictures/' +\
                self.user.username + '.jpg'
            if os.path.isfile(filename):
                return picture_url
            else:
                gravatar_url = 'http://www.gravatar.com/avatar/{0}?{1}'.format(
                    hashlib.md5(self.user.email.lower()).hexdigest(),
                    urllib.urlencode({'d': no_picture, 's': '256'})
                    )
                return gravatar_url

        except Exception:
            return no_picture


@python_2_unicode_compatible
class EmergencyContact(models.Model):
    emergencyContactFirstName = models.CharField("First Name", default="John", max_length=50, null=True, blank=True)
    emergencyContactLastName = models.CharField("Last Name", default="Doe", max_length=50, null=True, blank=True)
    emergnecyContactRelationship = models.CharField("Relationship", default="Child", max_length=50, null=True, blank=True)
    emergencyContactPhoneNumber = models.CharField("Phone Number", default="123-456-7890", max_length=12, null=True, blank=True)
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-emergencyContactLastName',)

    def __str__(self):
        return (self.emergencyContactFirstName, self.emergencyContactLastName)
