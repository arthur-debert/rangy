from rangy import Converter, TypeRegistry

# Create converters for built-in types

def register_builtins():
    int_converter = Converter(int)
    float_converter = Converter(float)
    converters = [int_converter, float_converter]
    for converter in converters:
        try:
            TypeRegistry.get(converter.type)
        except KeyError:
            TypeRegistry.register(converter)

register_builtins()