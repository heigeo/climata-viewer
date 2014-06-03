from wq.db.patterns import models
from wq.db.contrib.vera.models import BaseSite


class Site(models.IdentifiedModel, BaseSite):
    pass


class State(models.IdentifiedModel):
    pass


class County(models.IdentifiedModel):
    class Meta:
        verbose_name_plural = "counties"


class Basin(models.IdentifiedModel):
    class Meta:
        ordering = ("primary_identifiers__slug",)
