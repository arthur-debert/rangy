from rangy import Converter, ConverterRegistry

# Create converters for built-in types

def register_builtins():
    int_converter = Converter(int)
    float_converter = Converter(float)
    converters = [int_converter, float_converter]
    for converter in converters:
        try:
            ConverterRegistry.get(converter._type)
        except KeyError:
            ConverterRegistry.register(converter)

register_builtins()