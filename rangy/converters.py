class Converter():
    """
    Rangy can work with any type that implements a numerical conversion (i.e. __int__ or __float) and a string convertion ( __str__  or __repr__), method.

    Additionally, if the object does not implement those, the equivalent functions can be passed as arguments to the constructor.

    Args:
        type (type): Type of the object.
        to_numeric (function): Function that converts the object to a numerical value.
        to_string (function): Function that converts the object to a string value.
    """
    def __init__(self, type, to_numeric=None, to_string=None):
        self.type = type
        self.to_numeric = to_numeric
        self.to_string = to_string

    def to_number(self, value):
        if self.to_numeric:
            return self.to_numeric(value)
        try:
            return float(value)
        except ValueError:
            try:
                return int(value)
            except ValueError:
                raise ValueError("Could not convert value to number")

    def to_str(self, value):
        if self.to_string:
            return self.to_string(value)
        return str(value)

    def __float__(self, value):
        return self.to_number(value)

    def __int__(self, value):
        return self.to_number(value)

    def __str__(self, value):
        return self.to_str(value)

    def __call__(self, value):
        return self.to_number(value)