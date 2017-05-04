import inspect
from mongoengine import Document, EmbeddedDocument


def is_valid_mongoengine_document(document):
    return inspect.isclass(document) and (issubclass(document, Document) or issubclass(document, EmbeddedDocument))


def get_document_fields(document):
    return document._fields


def get_type_for_document(schema, document):
    types = schema.types.values()
    for _type in types:
        type_document = hasattr(_type, '_meta') and getattr(
            _type._meta, 'document', None)
        if document == type_document:
            return _type
