from django import template

register = template.Library()


@register.inclusion_tag('tags/alert.html', name="display_alert")
def display_alert(level: str, text: str):
    return {
        "level": level,
        "text": text,
    }
