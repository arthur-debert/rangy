from rangy import Converter, TypeRegistry

# Create converters for built-in types
int_converter = Converter(int)
float_converter = Converter(float)

converters = [int_converter, float_converter]
for converter in converters:
    if not TypeRegistry.get(converter.type):
        TypeRegistry.register(converter)