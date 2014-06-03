from wq.db.contrib.dbio.models import IoModel
from wq.db.contrib.dbio.signals import import_complete
from wq.db.patterns import models
from wq.db.rest.models import get_object_id
from wq.io.util import flattened

from django.dispatch import receiver
from rest_framework.settings import import_from_string
import datetime


DEFAULT_OPTIONS = (
    'start_date',
    'end_date',
    'state',
    'county',
    'basin',
    'station',
    'parameter',
)


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

    def describe_option(self, option, name=None):
        return {
            'name': name,
            'ignored': option.ignored,
            'required': option.required,
            'multi': option.multi,
        }

    @property
    def default_options(self):
        options = {}
        io_options = self.io_class.get_filter_options()
        for name in DEFAULT_OPTIONS:
            if name not in io_options:
                raise Exception(
                    "%s is missing %s option!"
                    % (self.class_name, name)
                )
            options[name] = self.describe_option(io_options[name], name)
        return options

    @property
    def extra_options(self):
        options = []
        for name, option in self.io_class.get_filter_options().items():
            if name in DEFAULT_OPTIONS:
                continue
            options.append(self.describe_option(option, name))
        return options


class DataRequest(IoModel):
    user = models.ForeignKey('auth.User', null=True, blank=True)
    webservice = models.ForeignKey(Webservice)
    requested = models.DateTimeField(auto_now=True)
    completed = models.DateTimeField(null=True, blank=True)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def load_io(self):
        if hasattr(self, '_loaded_io'):
            return self._loaded_io
        options = self.get_io_options()
        self._loaded_io = flattened(self.webservice.io_class, **options)
        return self._loaded_io

    def get_io_options(self):
        opt_values = {
            'debug': True,
        }
        for field in DEFAULT_OPTIONS:
            value = getattr(self, field)
            if isinstance(value, models.Model):
                opt_values[field] = get_object_id(value)
            else:
                opt_values[field] = value
        return opt_values

    def __unicode__(self):
        if not self.webservice_id:
            return None
        if self.basin:
            locs = ", ".join(self.basin)
        elif self.station:
            locs = ", ".join(self.station)
        else:
            locs = "SOMEWHERE"

        return "%s data for %s from %s to %s" % (
            self.webservice,
            locs,
            self.start_date,
            self.end_date,
        )

    def get_filter_ids(self, name):
        rels = self.inverserelationships.filter(from_content_type__name=name)
        if not rels.count():
            return None
        return [get_object_id(rel.right) for rel in rels]

    @property
    def state(self):
        return None

    @property
    def county(self):
        return None

    @property
    def basin(self):
        return self.get_filter_ids('region')

    @property
    def station(self):
        return self.get_filter_ids('site')

    @property
    def parameter(self):
        return self.get_filter_ids('parameter')

    class Meta:
        ordering = ("-requested",)


@receiver(import_complete)
def on_import_complete(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance:
        instance.completed = datetime.datetime.now()
        instance.save()
