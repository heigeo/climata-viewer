from wq.db.rest.serializers import ModelSerializer
from wq.db.rest.auth.serializers import UserSerializer


class DataRequestSerializer(ModelSerializer):
    class Meta:
        exclude = ("relationships", "inverserelationships")


class UserSerializer(UserSerializer):
    class Meta:
        exclude = ("vera_report",)
