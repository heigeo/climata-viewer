from wq.db.patterns import models
from vera.models import BaseSite
from django.contrib.gis.geos import Point


class SiteManager(models.IdentifiedRelatedModelManager):
    def near(self, latitude, longitude, degrees=0.01):
        # FIXME: Real-world distance in degrees is different for lat/lng;
        # this works good enough though so whatever
        sites = self.filter(
            latitude__gt=latitude-degrees,
            latitude__lt=latitude+degrees,
            longitude__gt=longitude-degrees,
            longitude__lt=longitude+degrees,
        )
        loc = Point(longitude, latitude, srid=4326)

        return sorted(
            sites,
            key=lambda c: loc.distance(
                Point(c.longitude, c.latitude, srid=4326)
            )
        )


class Site(models.IdentifiedRelatedModel, BaseSite):
    name = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    objects = SiteManager()


class State(models.IdentifiedModel):
    pass


class County(models.IdentifiedModel):
    state = models.ForeignKey(State, null=True)

    def __str__(self):
        label = super(County, self).__str__()
        if self.state and self.state.primary_identifier:
            return "%s, %s" % (label, self.state.primary_identifier.slug)
        return label

    class Meta:
        verbose_name_plural = "counties"


class Basin(models.IdentifiedModel):
    def __str__(self):
        return "%s %s" % (
            self.primary_identifier.slug, self.primary_identifier.name
        )

    class Meta:
        ordering = ("primary_identifiers__slug",)
