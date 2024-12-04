import pytest
from rangy import _normalize_range_input
from rangy.exceptions import ParseRangeError

@pytest.mark.parametrize("range_input, expected_output", [
    ((1, 2), (1, 2)),
    ([1, 2], (1, 2)),
    (1, (1, 1)),
    ("(1,2)", ("1", "2")),  # Strings remain strings after normalization.
    ("[1,2]", ("1", "2")),
    ("1,2", ("1", "2")),
    ("1", ("1", "1")),
    ("(1)", ("1", "1")),  # Single value in parentheses.
    ("[1]", ("1", "1")),
    ("  1 , 2  ", ("1", "2")), # Test with extra spaces
    ("1-2", ("1", "2")), # Hyphenated range.
])
def test_normalize_range_input_valid(range_input, expected_output):
    assert _normalize_range_input(range_input) == expected_output


@pytest.mark.parametrize("range_input", [
    (1, 2, 3),
    [1, 2, 3],
    "1,2,3",
    "1-2-3",
    1.5, # float
    {"a": 1}, # wrong type
])
def test_normalize_range_input_invalid(range_input):
    with pytest.raises(ParseRangeError):
        _normalize_range_input(range_input)




