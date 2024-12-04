import pytest

from rangy.exceptions import ParseRangeError
from rangy import parse_range


def test_str_single_integer():
    assert parse_range("5") == (5, 5)

