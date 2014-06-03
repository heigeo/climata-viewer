from rest_framework.fields import Field, SerializerMethodField
from rest_framework.serializers import ValidationError
from wq.db.rest.serializers import ModelSerializer
from wq.db.rest.auth.serializers import UserSerializer
from .models import Webservice


class WebserviceSerializer(ModelSerializer):
    opts = Field("default_options")
    extra_opts = Field("extra_options")


class DataRequestSerializer(ModelSerializer):
    def validate_option(self, attrs, field):
        if not attrs.get('webservice', None):
            return attrs

        webservice = attrs['webservice']
        opts = webservice.default_options[field]
        if not attrs.get(field, None) and opts['required']:
            raise ValidationError(
                "This field is required for this webservice."
            )
        return attrs

    def validate_start_date(self, attrs, source):
        return self.validate_option(attrs, source)

    def validate_end_date(self, attrs, source):
        return self.validate_option(attrs, source)

    class Meta:
        exclude = ("relationships",)


class UserSerializer(UserSerializer):
    class Meta:
        exclude = ("vera_report",)


class AuthedModelSerializer(ModelSerializer):
    authority_id = SerializerMethodField("get_authority_id")

    def get_authority_id(self, instance):
        return instance.primary_identifier.authority_id
