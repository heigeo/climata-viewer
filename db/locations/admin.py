from wq.db.patterns import admin
from .models import Site, Region

admin.site.register(Site, admin.IdentifiedModelAdmin)
admin.site.register(Region, admin.IdentifiedModelAdmin)
