from wq.db.contrib.dbio.models import IoModel
from wq.db.contrib.dbio.signals import import_complete
from wq.db.patterns import models
from wq.io.util import flattened

from django.dispatch import receiver
from rest_framework.settings import import_from_string
import datetime


class Webservice(models.Model):
    name = models.CharField(max_length=255)
    homepage = models.URLField()
    authority = models.ForeignKey('identify.Authority')
    class_name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    @property
    def io_class(self):
        return import_from_string(self.class_name, self.name)


class DataRequest(IoModel):
    user = models.ForeignKey('auth.User', null=True, blank=True)
    webservice = models.ForeignKey(Webservice)
    requested = models.DateTimeField(auto_now=True)
    completed = models.DateTimeField(null=True, blank=True)
    region = models.ForeignKey('locations.Region', null=True, blank=True)
    date_start = models.DateField()
    date_end = models.DateField()

    def load_io(self):
        options = self.get_io_options()
        return flattened(self.webservice.io_class, **options)

    def get_io_options(self):
        return {
            'sdate': self.date_start,
            'edate': self.date_end,
            'basin': self.region.primary_identifier.slug,
            'elems': ['avgt', 'pcpn'],
            'debug': True,
        }

    def __unicode__(self):
        if self.webservice_id and self.region_id:
            return "%s data for %s from %s to %s" % (
                self.webservice,
                self.region,
                self.date_start,
                self.date_end,
            )
        else:
            return "Request"

    class Meta:
        ordering = ("-requested",)


@receiver(import_complete)
def on_import_complete(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance:
        instance.completed = datetime.datetime.now()
        instance.save()
