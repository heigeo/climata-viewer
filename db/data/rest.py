from .models import Webservice, DataRequest
from .serializers import DataRequestSerializer, UserSerializer
from wq.db.patterns.models import (
    Relationship, InverseRelationship, RelationshipType
)
from wq.db.contrib.dbio.views import IoViewSet
from wq.db.rest import app
from django.contrib.auth.models import User


app.router.register_model(Webservice)
app.router.register_model(
    DataRequest,
    viewset=IoViewSet,
    serializer=DataRequestSerializer,
    reversed=True,
)
app.router.register_serializer(User, UserSerializer)

app.router.register_queryset(RelationshipType, RelationshipType.objects.none())
app.router.register_queryset(Relationship, Relationship.objects.none())
app.router.register_queryset(
    InverseRelationship, InverseRelationship.objects.none()
)
