from rangy import ANY_CHAR, AT_LEAST_ONE_CHAR, INFINITY, SPECIAL_CHARS
from rangy.exceptions import ParseRangeError


import re
from typing import Tuple, Union


def _parse(self, rangy) -> Tuple[Union[int, float], Union[int, float]]:
    """
    Parses a rangy specification into a tuple representing the min and max allowed rangys.

    Args:
        rangy: The rangy specification. Can be one of the following:
            - int: An exact rangy.
            - str: A string representation of an exact rangy or a range.  Ranges can be specified as "min-max", "min+", "+", or "*".  Uses '-', ',', ':', and ';' as separators.
            - tuple: A two-element tuple (min, max) representing the range.  Elements can be int or str.

    Returns:
        A tuple (min_count, max_count) representing the parsed count range.  `INFINITY` is used for open maximums.

    Raises:
        ParseRangeError: If the provided `rangy` is in an invalid format, such as an incorrect range string, a tuple with more than two elements, or non-numeric values.

    Examples:
        - 4  # An integer
        - "4" # A string representing an integer
        - "*"  # Any count
        - "+" # At least one
        - "1-3" # A range
        - (1, 3)  # A tuple range
        - ("1", "3") # A tuple range with strings
        - ("4", "*") # Open-ended range
    """
    range_pattern = re.compile(r"^(\d+|\*|\+)[-,:;](\d+|\*|\+)$")

    if isinstance(rangy, tuple) and len(rangy) == 2:
        min_val, max_val = rangy
        if min_val is None or max_val is None:
            raise ParseRangeError(f"Invalid rangy specification: {rangy}")
    elif isinstance(rangy, str) and range_pattern.match(rangy):
        min_val, max_val = range_pattern.match(rangy).groups()
    elif isinstance(rangy, str) and any(sep in rangy for sep in "-,:;"):
        raise ParseRangeError(f"Invalid rangy specification: {rangy}")
    elif isinstance(rangy, (int, str)):
        if rangy in SPECIAL_CHARS.values():
            min_val = rangy
            max_val = rangy
        else:
            try:
                min_val = max_val = int(rangy)
            except ValueError:
                raise ParseRangeError(f"Invalid rangy specification: {rangy}")
    elif rangy == ANY_CHAR:
        min_val = 0
        max_val = INFINITY
    elif rangy == AT_LEAST_ONE_CHAR:
        min_val = 1
        max_val = INFINITY
    else:
        raise ParseRangeError(f"Invalid rangy specification: {rangy}")

    chars = SPECIAL_CHARS.values()
    min_val = int(min_val) if min_val not in chars else min_val
    max_val = int(max_val) if max_val not in chars  else max_val

    if min_val == '*':
        min_val = 0
    elif min_val == '+':
        min_val = 1

    if max_val == '*':
        max_val = INFINITY
    elif max_val == '+':
        max_val = INFINITY

    if min_val < 0 or max_val < 0:
        raise ParseRangeError(f"Rangys are always positive, got {min_val}, {max_val}")

    return min_val, max_val