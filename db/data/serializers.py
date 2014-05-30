from rest_framework.fields import Field
from wq.db.rest.serializers import ModelSerializer
from wq.db.rest.auth.serializers import UserSerializer


class WebserviceSerializer(ModelSerializer):
    opts = Field("default_options")
    extra_opts = Field("extra_options")


class DataRequestSerializer(ModelSerializer):
    class Meta:
        exclude = ("relationships",)


class UserSerializer(UserSerializer):
    class Meta:
        exclude = ("vera_report",)
