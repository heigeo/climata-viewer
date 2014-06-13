from django.core.management.base import BaseCommand
from climata.fips import state_counties
from locations.models import County


class Command(BaseCommand):
    args = "<state>"
    help = "Import FIPS county codes"

    def handle(self, state, **options):
        counties = state_counties(state)
        for fips, info in counties.items():
            county = County.objects.find(fips)
            ident = county.primary_identifier
            ident.name = "%s, %s" % (info.countyname, info.state)
            ident.save()
