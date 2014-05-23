from wq.db.patterns import models
from wq.db.contrib.vera.models import BaseSite


class Site(models.IdentifiedModel, BaseSite):
    pass


class Region(models.IdentifiedModel):
    class Meta:
        ordering = ("primary_identifiers__slug",)
