import re
from rangy.exceptions import ParseRangeError
from rangy.registry import ConverterRegistry


def _split(as_squence):
    if len(as_squence) == 1:
        # this is valid, as it
        # indicates a single value range
        return as_squence[0], as_squence[0]
    elif len(as_squence) == 2:
        return as_squence[0], as_squence[1]
    else:
        raise ParseRangeError("Invalid range tuple/list length")


def _normalize_to_sequence(range_input):
    """Normalizes various range inputs into a consistent tuple representation.

    Args:
        range_input: The range input, which can be a string, tuple, int, etc.

    Returns:
        A tuple (start, end) representing the normalized range.

    Raises:
        ParseRangeError: If the input is invalid or cannot be normalized.
    """


    if isinstance(range_input, (tuple, list)):
        if len(range_input) == 1:
            return range_input[0], range_input[0]  # Single element tuple/list.
        elif len(range_input) == 2:
            return range_input[0], range_input[1]
        else:
            raise ParseRangeError("Invalid range tuple/list length")

    elif isinstance(range_input, int):
        return range_input, range_input  #

    elif isinstance(range_input, str):
        # treat the string.
        range_str = range_input.strip()
        if range_str.startswith("(") and range_str.endswith(")"):
            range_str = range_str[1:-1]
        elif range_str.startswith("[") and range_str.endswith("]"):
            range_str = range_str[1:-1]

        parts = re.split(r'[\s,;|-]+', range_str)  # Use regex to split by any whitespace, comma, semicolon, or hyphen.
        return _split(parts)
    else:
        raise ParseRangeError(f"Unsupported range input type: {type(range_input)}")


def _convert_string_part(part): # Helper function.
    for converter in ConverterRegistry():
        try:
            return converter(part)  # Use converter.parse() for strings.
        except (ValueError, TypeError):
            pass  # Try the next converter
    raise ParseRangeError("No suitable converter found for string part.")


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
        if not isinstance(start, str):
            converter = ConverterRegistry.get(start)
            parsed_start = converter(start) # or converter.to_number(start) depending on your Converter interface.
        else:
            parsed_start = _convert_string_part(start)

        if not isinstance(end, str):
            converter = ConverterRegistry.get(end)
            parsed_end = converter(end) # or converter.to_number(end)
        else:
            parsed_end = _convert_string_part(end)
        return parsed_start, parsed_end

    except (KeyError, ValueError, TypeError) as e:  # Handle converter and TypeRegistry errors.
        raise ParseRangeError(f"Error parsing range: {e}") from e