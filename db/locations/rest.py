from .models import Site, State, County, Basin
from data.serializers import AuthedModelSerializer
from wq.db.rest import app


# Compute whether it's feasible to cache all of the choices client side
def cache_opts(cls):
    # See http://wq.io/docs/config
    if cls.objects.count() > 250:
        return {'max_local_pages': 0, 'partial': True}
    else:
        return {'per_page': 250}

app.router.register_model(
    Site,
    serializer=AuthedModelSerializer,
    **cache_opts(Site)
)

app.router.register_model(County, **cache_opts(County))
app.router.register_model(Basin, **cache_opts(Basin))

# No cache_opts, there will probably never be more than 100 states
app.router.register_model(State, per_page=100)
