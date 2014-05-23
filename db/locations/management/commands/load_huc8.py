from wq.io import GisIO
from locations.models import Region
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = "<shapefile>"
    help = "Import HUC8 boundaries from USGS shapefile"

    def handle(self, shapefile, **options):
        watersheds = GisIO(filename=shapefile)
        for id, watershed in watersheds.items():
            region = Region.objects.find(watershed.huc_code)
            ident = region.primary_identifier
            ident.name = watershed.huc_name
            ident.save()
