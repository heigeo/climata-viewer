from .models import Webservice, DataRequest
from .serializers import (
    WebserviceSerializer, DataRequestSerializer, UserSerializer,
    AuthedModelSerializer, InverseRelationshipSerializer
)
from wq.db.patterns.models import (
    Relationship, InverseRelationship, RelationshipType
)
from wq.db.contrib.dbio.views import IoViewSet
from wq.db.rest import app
from django.contrib.auth.models import User
import swapper

Parameter = swapper.load_model('vera', 'Parameter')


def user_filter(qs, request):
    if request.user and request.user.is_authenticated():
        return qs.filter(user=request.user)
    else:
        return qs.none()

app.router.register_model(
    Webservice,
    serializer=WebserviceSerializer,
)
app.router.register_model(
    DataRequest,
    viewset=IoViewSet,
    filter=user_filter,
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
app.router.register_serializer(
    InverseRelationship,
    InverseRelationshipSerializer
)
