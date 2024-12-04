
from rangy.converters import Converter


class TypeRegistry:

    types = {}

    def __init__(self):
        TypeRegistry.types = {}

    @classmethod
    def register(cls, converter: Converter):
        cls.types[converter.type] = converter

    @classmethod
    def get(self, _type):
        # if type is not a type, try to get the type from the object
        if not isinstance(_type, type):
            _type = _type.__class__
        return self.types[_type]

    @classmethod
    def clear(self):
        self.types = {}