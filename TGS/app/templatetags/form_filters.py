from django import template

register = template.Library()

@register.filter
def add_class(field, css_class):
    """
    Adds a CSS class to a form field.
    Usage: {{ form.field|add_class:"css-class-name" }}
    """
    return field.as_widget(attrs={"class": css_class})

@register.filter
def multiply(value, arg):
    """Multiplies the value by the argument."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0