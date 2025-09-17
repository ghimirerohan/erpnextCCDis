

def split_decimal_parts(value):
    """
    Splits a float value according to new two-place decimal rules.
    
    Always returns a tuple (before_decimal, after_decimal) where:
    - before_decimal: the integer part before the decimal point
    - after_decimal: the decimal part as a two-digit number
    
    Examples: 
    - 0.02 -> (0, 2), 0.23 -> (0, 23), 0.10 -> (0, 10), 0.1 -> (0, 10), 0.01 -> (0, 1), 0.25 -> (0, 25), 0.2 -> (0, 20)
    - 4.08 -> (4, 8), 8.11 -> (8, 11), 6.1 -> (6, 10), 4.2 -> (4, 20)
    - 1 -> (1, 0), 2 -> (2, 0), 6 -> (6, 0)
    """
    value_str = str(value)
    
    if '.' in value_str:
        before_decimal, after_decimal = value_str.split('.')
        before_decimal = int(before_decimal)
        
        # Handle decimal part - ensure it's treated as two digits
        if len(after_decimal) == 1:
            # Single digit after decimal (e.g., 0.1, 6.1, 4.2) - treat as .10, .10, .20
            after_decimal = int(after_decimal + '0')
        else:
            # Multiple digits after decimal - take first two digits
            after_decimal = int(after_decimal[:2])
    else:
        before_decimal = int(value_str)
        after_decimal = 0
    
    # Always return a tuple (before_decimal, after_decimal)
    return before_decimal, after_decimal