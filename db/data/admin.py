from wq.db.patterns import admin
from .models import Webservice, DataRequest, Project


class DataRequestAdmin(admin.RelatedModelAdmin):
    list_display = ('__unicode__', 'webservice', 'user')
    list_filter = ('webservice', 'user')

admin.site.register(Webservice, admin.IdentifiedModelAdmin)
admin.site.register(DataRequest, DataRequestAdmin)
admin.site.register(Project, admin.IdentifiedRelatedModelAdmin)
