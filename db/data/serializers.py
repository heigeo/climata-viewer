from rest_framework.fields import Field, SerializerMethodField
from rest_framework.serializers import (
    ValidationError, Field, SerializerMethodField
)
from wq.db.rest.serializers import ModelSerializer
from wq.db.rest.auth.serializers import UserSerializer
from wq.db.patterns.relate.serializers import (
    RelationshipSerializer,
    InverseRelationshipSerializer
)
from vera.serializers import EventResultSerializer
from wq.db.patterns.models import Relationship, RelationshipType
from .models import Webservice, Project
from django.utils.crypto import get_random_string


class WebserviceSerializer(ModelSerializer):
    opts = Field("default_options")
    extra_opts = Field("extra_options")
    source_url = Field()


class MySerializer(ModelSerializer):
    mine = SerializerMethodField('get_mine')

    def from_native(self, data, files):
        if 'user' not in data:
            data = data.copy()
            user = self.context['request'].user
            data['user'] = user.pk
        return super(MySerializer, self).from_native(data, files)

    def get_mine(self, instance):
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

    def from_native(self, data, files):
        # Create project on the fly
        project_name = data.get('project-name', None)
        if project_name:
            project, is_new = Project.objects.get_or_create_by_natural_key(
                project_name
            )
            if not is_new:
                project_name += " " + get_random_string(5)
                project = Project.objects.find(project_name)
            project_id = project.primary_identifier.slug
            user = self.context['request'].user
            project.name = project_name
            project.user_id = user.pk
            project.save()
            reltype = RelationshipType.objects.get(from_type__name='project')
            data = data.copy()
            data['inverserelationship-%s-item_id' % reltype.pk] = project_id

        return super(DataRequestSerializer, self).from_native(data, files)

    def save(self, *args, **kwargs):
        result = super(DataRequestSerializer, self).save(*args, **kwargs)
        if getattr(self, 'object', None) and self.object.project:
            self.object.public = self.object.project.public
            self.object.save()
        return result

    class Meta:
        exclude = ("relationships",)


class RelationshipSerializer(RelationshipSerializer):
    class Meta:
        model = Relationship


class ProjectSerializer(MySerializer):
    has_data = Field()
    def get_default_fields(self):
        fields = super(ProjectSerializer, self).get_default_fields()
        if 'request' in self.context and self.context['request'].POST:
            pass
        else:
            fields['relationships'] = RelationshipSerializer(
                source="active_rels",
            )
        return fields


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
        if '\xa0' in ident:
            ident = ident.split('\xa0')[1]
            data[fields['item_id']] = ident
        return super(InverseRelationshipSerializer, self).create_dict(
            atype, data, fields, index
        )
