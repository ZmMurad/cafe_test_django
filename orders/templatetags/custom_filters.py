from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Умножает два числа в шаблоне."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
