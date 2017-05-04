from mongoengine import fields

from graphene import Boolean, Float, Int, List, String, Dynamic, NonNull
from graphene.relay import is_node

from graphene_django.utils import import_single_dispatch

from .fields import (
    MongoEngineDocumentField, get_connection_field,
    MongoEngineListField)


singledispatch = import_single_dispatch()


@singledispatch
def convert_mongoengine_field(field, registry=None):
    raise Exception(
        "Don't know how to convert the MongoEngine field %s (%s)" % (field, field.__class__))


@convert_mongoengine_field.register(fields.StringField)
@convert_mongoengine_field.register(fields.URLField)
@convert_mongoengine_field.register(fields.EmailField)
@convert_mongoengine_field.register(fields.DateTimeField)
@convert_mongoengine_field.register(fields.ComplexDateTimeField)
@convert_mongoengine_field.register(fields.BinaryField)
@convert_mongoengine_field.register(fields.FileField)
@convert_mongoengine_field.register(fields.ImageField)
@convert_mongoengine_field.register(fields.UUIDField)
def convert_field_to_string(field, registry=None):
    return String()


@convert_mongoengine_field.register(fields.ObjectIdField)
def convert_field_to_id(field, registry=None):
    return String()


@convert_mongoengine_field.register(fields.IntField)
@convert_mongoengine_field.register(fields.LongField)
def convert_field_to_int(field, registry=None):
    return Int()


@convert_mongoengine_field.register(fields.BooleanField)
def convert_field_to_boolean(field, registry=None):
    return Boolean()


@convert_mongoengine_field.register(fields.FloatField)
@convert_mongoengine_field.register(fields.DecimalField)
def convert_field_to_float(field, registry=None):
    return Float()


@convert_mongoengine_field.register(fields.ListField)
@convert_mongoengine_field.register(fields.SortedListField)
def convert_field_to_graphql_list(field, registry=None):

    def dynamic_type():
        base_type = convert_mongoengine_field(field.field)
        if not isinstance(base_type, (List, NonNull, Dynamic)):
            base_type = type(base_type)
            return List(base_type)
        if isinstance(base_type, Dynamic):
            _type = registry.get_type_for_model(field.field.document_type)
            return MongoEngineListField(_type)

    return Dynamic(dynamic_type)


@convert_mongoengine_field.register(fields.EmbeddedDocumentListField)
def convert_field_to_graphql_list_field(field, registry=None):

    def dynamic_type():
        _type = registry.get_type_for_model(field.field.document_type)
        if not _type:
            return

        if is_node(_type):
            return get_connection_field(_type)

        return MongoEngineListField(_type)

    return Dynamic(dynamic_type)


@convert_mongoengine_field.register(fields.EmbeddedDocumentField)
@convert_mongoengine_field.register(fields.ReferenceField)
def convert_field_to_graphql_field(field, registry=None):
    def dynamic_type():
        document = field.document_type
        _type = registry.get_type_for_model(field.document_type)
        if not _type:
            return
        return MongoEngineDocumentField(document, _type)

    return Dynamic(dynamic_type)
