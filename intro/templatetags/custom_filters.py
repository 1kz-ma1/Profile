from django import template

register = template.Library()

@register.filter
def image_url(image_field):
    """Safely get image URL, returns empty string if not available"""
    if image_field:
        try:
            return image_field.url
        except (AttributeError, ValueError):
            return ''
    return ''
