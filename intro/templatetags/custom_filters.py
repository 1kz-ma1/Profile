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

@register.filter
def truncate_lines(text, num_lines=3):
    """Truncate text to specified number of lines and add ellipsis"""
    if not text:
        return ''
    lines = text.split('\n')
    if len(lines) > num_lines:
        return '\n'.join(lines[:num_lines]) + '...'
    # Split by sentence period if fewer lines but too long
    full_text = '\n'.join(lines[:num_lines])
    sentences = full_text.replace('\n', ' ').split('。')
    if len(sentences) > 1:
        result = '。'.join(sentences[:2]) + '。'
        if len(result) > 200:  # Limit character length
            result = result[:200] + '...'
        return result
    return full_text
