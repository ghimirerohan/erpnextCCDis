

def split_decimal_parts(value):
    """
    Splits a float value into integer and fractional parts as integers.
    Example: 10.05 -> (10, 5)
    """
    value_str = str(value)
    if '.' in value_str:
        before_decimal, after_decimal = value_str.split('.')
        before_decimal = int(before_decimal)
        # Remove leading/trailing zeros, then convert to int (if empty, set to 0)
        after_decimal = int(after_decimal or '0')
    else:
        before_decimal = int(value_str)
        after_decimal = 0
    return before_decimal, after_decimal