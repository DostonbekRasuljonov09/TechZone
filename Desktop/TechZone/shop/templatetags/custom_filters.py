from django import template

register = template.Library()

@register.filter
def trim(value):
    return value.strip() if value else value

@register.filter
def split_pipe(value):
    """Split a string by '|' separator"""
    if value:
        return [s.strip() for s in value.split('|')]
    return []
