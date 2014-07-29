from wq.db.patterns import models
from wq.db.contrib.vera.models import BaseSite
from django.contrib.gis.geos import Point


class SiteManager(models.IdentifiedModelManager):
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


class Site(models.IdentifiedModel, BaseSite):
    name = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    objects = SiteManager()


class State(models.IdentifiedModel):
    pass


class County(models.IdentifiedModel):
    class Meta:
        verbose_name_plural = "counties"


class Basin(models.IdentifiedModel):
    class Meta:
        ordering = ("primary_identifiers__slug",)
