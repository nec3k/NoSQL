from django import template

register = template.Library()


@register.inclusion_tag('tags/button.html', name="display_button")
def display_button(text: str):
    return {
        "text": text,
    }
