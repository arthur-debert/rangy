from rangy.converters import Converter

class TypeRegistry:

    types = {}

    @classmethod
    def register(cls, converter: Converter):
        cls.types[converter.type] = converter

    @classmethod
    def get(cls, _type):
        # if type is not a type, try to get the type from the object
        if not isinstance(_type, type):
            _type = _type.__class__
        return cls.types[_type]

    @classmethod
    def clear(cls):
        cls.types = {}

    @classmethod
    def __iter__(cls):
        return iter(cls.types.values())
