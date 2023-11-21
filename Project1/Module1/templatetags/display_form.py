from django import template

register = template.Library()


@register.inclusion_tag('tags/form.html', name="display_form")
def display_form(form, action_url_name: str, submit_button_text: str):
    return {
        "form": form,
        "action_url_name": action_url_name,
        "submit_button_text": submit_button_text,       

    }
