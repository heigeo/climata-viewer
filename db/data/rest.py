from .models import Webservice, DataRequest
from .serializers import (
    WebserviceSerializer, DataRequestSerializer, UserSerializer,
    AuthedModelSerializer, InverseRelationshipSerializer
)
from .views import DataRequestViewSet
from wq.db.patterns.models import (
    Relationship, InverseRelationship, RelationshipType
)
from wq.db.rest import app
from django.contrib.auth.models import User
import swapper

Parameter = swapper.load_model('vera', 'Parameter')


def user_filter(qs, request):
    public_data = qs.filter(public=True)
    if request.user and request.user.is_authenticated():
        user_data = qs.filter(user=request.user)
    else:
        user_data = qs.none()

    return public_data | user_data


def rel_filter(qs, request):
    reqs = user_filter(DataRequest.objects.all(), request)
    return qs.filter(to_object_id__in=reqs.values_list('id', flat=True))

app.router.register_model(
    Webservice,
    serializer=WebserviceSerializer,
)
app.router.register_model(
    DataRequest,
    viewset=DataRequestViewSet,
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
app.router.register_filter(InverseRelationship, rel_filter)
app.router.update_config(InverseRelationship, per_page=10000)
app.router.register_serializer(
    InverseRelationship,
    InverseRelationshipSerializer
)
