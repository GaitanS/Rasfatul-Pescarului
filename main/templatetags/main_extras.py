from django import template
from datetime import datetime

register = template.Library()

ROMANIAN_DAYS = {
    'Monday': 'Luni',
    'Tuesday': 'Marți',
    'Wednesday': 'Miercuri',
    'Thursday': 'Joi',
    'Friday': 'Vineri',
    'Saturday': 'Sâmbătă',
    'Sunday': 'Duminică'
}

ROMANIAN_MONTHS = {
    'January': 'Ianuarie',
    'February': 'Februarie',
    'March': 'Martie',
    'April': 'Aprilie',
    'May': 'Mai',
    'June': 'Iunie',
    'July': 'Iulie',
    'August': 'August',
    'September': 'Septembrie',
    'October': 'Octombrie',
    'November': 'Noiembrie',
    'December': 'Decembrie'
}

@register.filter
def romanian_date(value):
    """Convert date to Romanian format"""
    if not value:
        return ''
    
    # Format date in English first
    english_date = value.strftime('%A, %d %B').replace(' 0', ' ')
    
    # Replace day and month names with Romanian equivalents
    for eng, rom in ROMANIAN_DAYS.items():
        english_date = english_date.replace(eng, rom)
    for eng, rom in ROMANIAN_MONTHS.items():
        english_date = english_date.replace(eng, rom)
    
    return english_date

@register.filter
def sub(value, arg):
    """Subtract the arg from the value"""
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return value

@register.filter
def multiply(value, arg):
    """Multiply the value by the arg"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return value

@register.filter
def divide(value, arg):
    """Divide the value by the arg"""
    try:
        return float(value) / float(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return value
