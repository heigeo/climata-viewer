from .models import Site, State, County, Basin
from data.serializers import AuthedModelSerializer
from wq.db.rest import app

app.router.register_model(
    Site,
    serializer=AuthedModelSerializer,
    per_page=10000
)
app.router.register_model(State, per_page=10000)
app.router.register_model(County, per_page=10000)
app.router.register_model(Basin, per_page=10000)
