import pytest
from rangy.parse import parse_range
from rangy.exceptions import ParseRangeError

def test_single_integer():
    assert parse_range("5") == (5, 5)
