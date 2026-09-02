from decimal import Decimal, ROUND_CEILING, ROUND_HALF_UP, InvalidOperation

TWOPLACES = Decimal("0.01")


def round_money(amount) -> float:
	"""Clamp to 2 decimal places (paisa). Never return float noise like 150.3700000002."""
	try:
		value = Decimal(str(amount if amount is not None else 0))
	except (InvalidOperation, ValueError, TypeError):
		return 0.0
	return float(value.quantize(TWOPLACES, rounding=ROUND_HALF_UP))


def ceil_rupees(amount) -> int:
	"""Whole rupees, rounding UP. 100.00 -> 100, 100.01 -> 101. Zero/negative -> 0."""
	try:
		value = Decimal(str(amount if amount is not None else 0))
	except (InvalidOperation, ValueError, TypeError):
		return 0
	if value <= 0:
		return 0
	return int(value.to_integral_value(rounding=ROUND_CEILING))
