from django.core.management.base import NoArgsCommand
import json
from wq.db.rest import app


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        app.autodiscover()
        print json.dumps(app.router.get_config())
