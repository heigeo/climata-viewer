from django.core.management.base import BaseCommand
from wq.io import GisIO
from climata.huc8 import get_huc8
from locations.models import Basin


class Command(BaseCommand):
    args = "<shapefile> <basin>"
    help = "Import HUC8 boundaries from USGS shapefile"

    def handle(self, shapefile, code, **options):
        watersheds = GisIO(filename=shapefile)
        huc8s = get_huc8(code)
        for id, watershed in watersheds.items():
            if watershed.huc_code not in huc8s:
                continue
            basin = Basin.objects.find(watershed.huc_code)
            ident = basin.primary_identifier
            ident.name = watershed.huc_name
            ident.save()

            # FIXME: actually do something with boundary
