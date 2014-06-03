from .models import Webservice, DataRequest
from .serializers import (
    WebserviceSerializer, DataRequestSerializer, UserSerializer,
    AuthedModelSerializer
)
from wq.db.patterns.models import (
    Relationship, InverseRelationship, RelationshipType
)
from wq.db.contrib.dbio.views import IoViewSet
from wq.db.rest import app
from django.contrib.auth.models import User
import swapper

Parameter = swapper.load_model('vera', 'Parameter')


app.router.register_model(
    Webservice,
    serializer=WebserviceSerializer,
)
app.router.register_model(
    DataRequest,
    viewset=IoViewSet,
    serializer=DataRequestSerializer,
    reversed=True,
)
app.router.register_serializer(User, UserSerializer)
app.router.register_serializer(Parameter, AuthedModelSerializer)

app.router.register_queryset(
    RelationshipType,
    RelationshipType.objects.filter(name="Filter For")
)
app.router.register_queryset(Relationship, Relationship.objects.none())
app.router.register_queryset(
    InverseRelationship,
    InverseRelationship.objects.filter(type__name="Filter For"),
)
