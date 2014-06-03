from wq.db.patterns import admin
from .models import Site, State, County, Basin

admin.site.register(Site, admin.IdentifiedModelAdmin)
admin.site.register(State, admin.IdentifiedModelAdmin)
admin.site.register(County, admin.IdentifiedModelAdmin)
admin.site.register(Basin, admin.IdentifiedModelAdmin)
