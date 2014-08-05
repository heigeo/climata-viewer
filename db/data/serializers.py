from rest_framework.fields import Field, SerializerMethodField
from rest_framework.serializers import (
    ValidationError, Field, SerializerMethodField
)
from wq.db.rest.serializers import ModelSerializer
from wq.db.rest.auth.serializers import UserSerializer
from wq.db.patterns.relate.serializers import InverseRelationshipSerializer
from wq.db.contrib.chart.serializers import EventResultSerializer
from .models import Webservice


class WebserviceSerializer(ModelSerializer):
    opts = Field("default_options")
    extra_opts = Field("extra_options")


class MySerializer(ModelSerializer):
    is_mine = SerializerMethodField('get_is_mine')

    def from_native(self, data, files):
        if 'user' not in data:
            data = data.dict()
            user = self.context['request'].user
            data['user'] = user.pk
        return super(MySerializer, self).from_native(data, files)

    def get_is_mine(self, instance):
        if 'request' in self.context:
            if self.context['request'].user == instance.user:
                return True
        return False


class DataRequestSerializer(MySerializer):
    as_python = Field()

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


class ProjectSerializer(MySerializer):
    has_data = Field()


class UserSerializer(UserSerializer):
    class Meta:
        exclude = ("vera_report",) + UserSerializer.Meta.exclude


class AuthedModelSerializer(ModelSerializer):
    authority_id = SerializerMethodField("get_authority_id")

    def get_authority_id(self, instance):
        return set([
            ident.authority_id
            for ident in instance.identifiers.all()
            if ident.authority_id is not None
        ])


class InverseRelationshipSerializer(InverseRelationshipSerializer):
    def create_dict(self, atype, data, fields, index):
        ident = data[fields['item_id']]
        if u'\xa0' in ident:
            ident = ident.split(u'\xa0')[1]
            data[fields['item_id']] = ident
        return super(InverseRelationshipSerializer, self).create_dict(
            atype, data, fields, index
        )
