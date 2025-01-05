from django import template

register = template.Library()

@register.filter
def stars(value):
    """Generate a string of star emojis based on the rating value."""
    try:
        return '⭐' * int(value)
    except (ValueError, TypeError):
        return ''
