from wq.db.patterns import admin
from .models import Webservice, DataRequest

admin.site.register(Webservice, admin.IdentifiedModelAdmin)
admin.site.register(DataRequest, admin.RelatedModelAdmin)
