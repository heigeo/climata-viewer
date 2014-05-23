from wq.db.patterns import admin
from .models import Webservice

admin.site.register(Webservice, admin.IdentifiedModelAdmin)
