from wq.db.patterns import models
from wq.db.contrib.vera.models import BaseSite


class Site(models.IdentifiedModel, BaseSite):
    name = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)


class State(models.IdentifiedModel):
    pass


class County(models.IdentifiedModel):
    class Meta:
        verbose_name_plural = "counties"


class Basin(models.IdentifiedModel):
    class Meta:
        ordering = ("primary_identifiers__slug",)
