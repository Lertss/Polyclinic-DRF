import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from Patient.models import CustomUser


WEEKDAYS = [
    (1, _("Monday")),
    (2, _("Tuesday")),
    (3, _("Wednesday")),
    (4, _("Thursday")),
    (5, _("Friday")),
    (6, _("Saturday")),
    (7, _("Sunday")),
]


class Doctor(models.Model):
    """
       Model of a doctor
       Created in a binding (based on) the CustomUser class
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100,null=False, blank=False)
    phone_general = models.CharField(null=False, blank=False)
    cabinet = models.CharField(max_length=6, null=False, blank=False)




class OpeningHours(models.Model):
    """Model of doctor's appointment times"""
    weekday = models.IntegerField(choices=WEEKDAYS)
    open_hour = models.TimeField()
    close_hour = models.TimeField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    class Meta:
        ordering = ('weekday', 'open_hour')
        unique_together = ('weekday', 'open_hour', 'close_hour')

    def __unicode__(self):
        return u'%s: %s - %s' % (self.get_weekday_display(),
                                 self.open_hour, self.close_hour)


