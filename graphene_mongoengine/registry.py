class Registry(object):

    def __init__(self):
        self._registry = {}
        self._registry_models = {}

    def register(self, cls):
        from .types import MongoEngineObjectType
        assert issubclass(
            cls, MongoEngineObjectType), 'Only MongoEngineObjectType can be registered, received "{}"'.format(
            cls.__name__)
        assert cls._meta.registry == self, 'Registry for a Model have to match.'
        # assert self.get_type_for_model(cls._meta.model) == cls, (
        #     'Multiple DjangoObjectTypes registered for "{}"'.format(cls._meta.model)
        # )
        self._registry[cls._meta.document] = cls

    def get_type_for_model(self, model):
        return self._registry.get(model)


mongoengine_registry = None


def get_global_registry():
    global mongoengine_registry
    if not mongoengine_registry:
        mongoengine_registry = Registry()
    return mongoengine_registry


def reset_global_registry():
    global mongoengine_registry
    mongoengine_registry = None
