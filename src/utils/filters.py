from decimal import Decimal


def format_currency(value):
    if value is None:
        return "0.00"
    try:
        if isinstance(value, str):
            value = float(value.replace(",", ""))
        elif isinstance(value, Decimal):
            value = float(value)
        return f"{value:,.2f}"
    except (ValueError, TypeError):
        return "Invalid"


def format_number(value):
    if value is None:
        return 0
    try:
        if isinstance(value, str):
            value = float(value.replace(",", ""))
        elif isinstance(value, Decimal):
            value = float(value)
        return value
    except (ValueError, TypeError):
        return "Invalid"
