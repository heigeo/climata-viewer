from .models import Webservice, DataRequest, Project
from .serializers import (
    WebserviceSerializer, DataRequestSerializer, UserSerializer,
    AuthedModelSerializer, InverseRelationshipSerializer,
    ProjectSerializer
)
from .views import ToggleViewSet, DataRequestViewSet
from wq.db.patterns.models import (
    Relationship, InverseRelationship, RelationshipType
)
from django.db.models import Q
from wq.db.rest import app
from django.contrib.auth.models import User
import swapper

Parameter = swapper.load_model('vera', 'Parameter')


def user_filter(qs, request):
    query = Q(public=True)
    if request.user and request.user.is_authenticated():
        query = query | Q(user=request.user)
    return qs.filter(query).exclude(deleted__isnull=False)


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
    map=True,
)
app.router.register_model(
    Project,
    viewset=ToggleViewSet,
    filter=user_filter,
    serializer=ProjectSerializer,
    reversed=True,
    map=True,
)
app.router.register_serializer(User, UserSerializer)
app.router.register_serializer(Parameter, AuthedModelSerializer)
app.router.update_config(Parameter, per_page=10000)

app.router.register_queryset(
    RelationshipType,
    RelationshipType.objects.filter(to_type__model="datarequest")
)
app.router.register_queryset(
    Relationship,
    Relationship.objects.filter(from_content_type__model="project"),
)
app.router.register_filter(Relationship, rel_filter)
app.router.update_config(Relationship, per_page=10000)
app.router.register_queryset(
    InverseRelationship,
    InverseRelationship.objects.filter(to_content_type__model="datarequest"),
)
app.router.register_filter(InverseRelationship, rel_filter)
app.router.update_config(InverseRelationship, per_page=10000)
app.router.register_serializer(
    InverseRelationship,
    InverseRelationshipSerializer
)
