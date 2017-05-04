from functools import partial

from django.db.models.query import QuerySet

from graphene.types import Field, List
from graphene.relay import ConnectionField, PageInfo
from graphql_relay.connection.arrayconnection import connection_from_list_slice

from graphene_django.utils import maybe_queryset

from .utils import get_type_for_document


class MongoEngineListField(Field):

    def __init__(self, _type, *args, **kwargs):
        super(MongoEngineListField, self).__init__(List(_type), *args, **kwargs)

    @property
    def model(self):
        return self.type.of_type._meta.node._meta.document

    @staticmethod
    def list_resolver(resolver, root, args, context, info):
        return maybe_queryset(resolver(root, args, context, info))

    def get_resolver(self, parent_resolver):
        return partial(self.list_resolver, parent_resolver)


class MongoEngineConnectionField(ConnectionField):

    def __init__(self, *args, **kwargs):
        self.on = kwargs.pop('on', False)
        super(MongoEngineConnectionField, self).__init__(*args, **kwargs)

    @property
    def model(self):
        return self.type._meta.node._meta.document

    def get_manager(self):
        if self.on:
            return getattr(self.model, self.on)
        else:
            return None

    @staticmethod
    def connection_resolver(resolver, connection, default_manager, root, args, context, info):
        iterable = resolver(root, args, context, info)
        if iterable is None:
            iterable = default_manager
        iterable = maybe_queryset(iterable)
        if isinstance(iterable, QuerySet):
            _len = iterable.count()
        else:
            _len = len(iterable)
        connection = connection_from_list_slice(
            iterable,
            args,
            slice_start=0,
            list_length=_len,
            list_slice_length=_len,
            connection_type=connection,
            edge_type=connection.Edge,
            pageinfo_type=PageInfo,
        )
        connection.iterable = iterable
        connection.length = _len
        return connection

    def get_resolver(self, parent_resolver):
        return partial(self.connection_resolver, parent_resolver, self.type, self.get_manager())


class MongoEngineDocumentField(Field):
    def __init__(self, document, *args, **kwargs):
        self.document = document
        super(MongoEngineDocumentField, self).__init__(*args, **kwargs)

    def internal_type(self, schema):
        _type = self.get_object_type(schema)
        if not _type and self.parent._meta.only_fields:
            raise Exception(
                    "Collection %r is not accessible by the schema. "
                    "You can either register the type manually "
                    "using @schema.register. "
                    "Or disable the field in %s" % (
                        self.document,
                        self.parent,
                    )
            )
        return schema.T(_type)

    def get_object_type(self, schema):
        return get_type_for_document(schema, self.document)

    @property
    def List(self):
        return List(self, *self.args, **self.kwargs)


def get_connection_field(*args, **kwargs):
    return MongoEngineConnectionField(*args, **kwargs)
