import re

from rangy.exceptions import ParseRangeError

from .const import INFINITY, SPECIAL_CHARS
from .registry import ConverterRegistry


def _split(as_squence):
    """
    Splits a sequence into a tuple of two values.
    It will ensure only sequences of length 1 or 2 are accepted and
    that no None values are present.

    Args:
        as_squence: The sequence to split, str, list, tuple.
    Raises:
        ParseRangeError: If the input is invalid.
    Returns:
        A tuple of two values.
    """
    if None in as_squence:
        raise ParseRangeError("Invalid range tuple/list")
    if len(as_squence) == 1:
        # this is valid, as it
        # indicates a single value range
        return as_squence[0], as_squence[0]
    elif len(as_squence) == 2:
        return as_squence[0], as_squence[1]
    else:
        raise ParseRangeError("Invalid range tuple/list length")

def _nomalize_str(range_str):
    """
    Normalizes a range string by removing brackets and splitting it into parts.

    "1-5" -> ["1", "5"]
    "(1-5)" -> ["1", "5"]
    "1-5" -> ["1", "5"]
    "(1,3)"

    Args:
        range_str: The range string to normalize.
    Returns:
        A tuples of parts of the range string.
    """
    range_str = re.sub(r'^[\[\(]|[\]\)]$', '', range_str.strip())  # Remove brackets
    range_str = re.split(r'[\s,;|-]+', range_str) # split
    return tuple(part.strip() for part in range_str if part.strip()) # Remove empty strings

def _normalize_to_sequence(range_input):
    """Normalizes various range inputs into a consistent tuple representation.

    Args:
        range_input: The range input, which can be a string, tuple, int, etc.

    Returns:
        A tuple (start, end) representing the normalized range.

    Raises:
        ParseRangeError: If the input is invalid or cannot be normalized.
    """
    from rangy import Rangy
    if isinstance(range_input, Rangy):
        range_input = range_input.copy().values

    if isinstance(range_input, (tuple, list)):
        return _split(range_input)
    elif isinstance(range_input, int):
        return range_input, range_input  #

    elif isinstance(range_input, str):
        return _split(_nomalize_str(range_input))
    else:
        raise ParseRangeError(f"Unsupported range input type: {type(range_input)}")


def _convert_part(part):
    if part in SPECIAL_CHARS.values():
        return part
    for converter in ConverterRegistry():
        try:
            return converter(part)
        except (ValueError, TypeError):
            pass  # Try the next converter
    raise ParseRangeError(f"No suitable converter found for string part: {part}")


def parse_range(range_input):
    """Parses a range into a tuple of converted (start, end) values.

    Args:
        range_input: The range input (string, tuple, int, etc.)

    Returns:
        A tuple (start, end) with converted values.

    Raises:
        ParseRangeError: If the input is invalid or cannot be parsed.
    """

    start, end = _normalize_to_sequence(range_input)

    try:
        return _convert_part(start), _convert_part(end)

    except (KeyError, ValueError, TypeError) as e:
        raise ParseRangeError(f"Error parsing range: {e}") from e