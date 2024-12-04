
import pytest

from rangy import Converter, TypeRegistry


def test_register_and_get_converter():
    registry = TypeRegistry()
    converter = Converter(int)
    registry.register(converter)
    assert registry.get(int) == converter

def test_get_converter_for_instance():
    registry = TypeRegistry()
    converter = Converter(int)
    registry.register(converter)
    assert registry.get(1) == converter

def test_get_nonexistent_converter():
    registry = TypeRegistry()
    with pytest.raises(KeyError):
        registry.get(str)

def test_clear_registry():
    registry = TypeRegistry()
    converter = Converter(int)
    registry.register(converter)
    registry.clear()
    with pytest.raises(KeyError):
        registry.get(int)