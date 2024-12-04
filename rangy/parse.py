from rangy.exceptions import ParseRangeError
from rangy.registry import TypeRegistry


def _normalize_range_input(range_input):
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
        return range_input, range_input  # Single integer.

    elif isinstance(range_input, str):
        range_str = range_input.strip()
        if range_str.startswith("(") and range_str.endswith(")"):
            range_str = range_str[1:-1]
        elif range_str.startswith("[") and range_str.endswith("]"):
            range_str = range_str[1:-1]

        parts = range_str.split(",")  # Handle hyphens later if needed.

        if len(parts) == 1:
            return parts[0], parts[0]
        elif len(parts) == 2:
            return parts[0], parts[1]
        else:
            raise ParseRangeError("Invalid range string format")
    else:
        raise ParseRangeError(f"Unsupported range input type: {type(range_input)}")


def _convert_string_part(part): # Helper function.
    for converter in TypeRegistry.values():
        try:
            return converter.parse(part)  # Use converter.parse() for strings.
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

    start, end = _normalize_range_input(range_input)

    try:
        if not isinstance(start, str):
            converter = TypeRegistry.get(start)
            parsed_start = converter(start) # or converter.to_number(start) depending on your Converter interface.
        else:
            parsed_start = _convert_string_part(start)

        if not isinstance(end, str):
            converter = TypeRegistry.get(end)
            parsed_end = converter(end) # or converter.to_number(end)
        else:
            parsed_end = _convert_string_part(end)
        return parsed_start, parsed_end

    except (KeyError, ValueError, TypeError) as e:  # Handle converter and TypeRegistry errors.
        raise ParseRangeError(f"Error parsing range: {e}") from e