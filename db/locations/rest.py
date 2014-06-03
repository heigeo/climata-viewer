from .models import Site, Region
from data.serializers import AuthedModelSerializer
from wq.db.rest import app

app.router.register_model(
    Site,
    serializer=AuthedModelSerializer,
    per_page=10000
)
app.router.register_model(Region, per_page=10000)
