from wq.db.patterns import admin
from .models import Site, State, County, Basin


class AuthedModelAdmin(admin.IdentifiedModelAdmin):
    list_display = ['__str__', 'authority']
    list_filter = ['identifiers__authority']

    def authority(self, instance):
        return ", ".join([
            str(ident.authority)
            for ident in instance.identifiers.all()
        ])

admin.site.register(Site, AuthedModelAdmin)
admin.site.register(State, admin.IdentifiedModelAdmin)
admin.site.register(County, admin.IdentifiedModelAdmin)
admin.site.register(Basin, admin.IdentifiedModelAdmin)
