from django import template

register = template.Library()


@register.inclusion_tag('tags/navbar_links.html', name="display_navbar_links")
def display_navbar_links(user, url_name:str, mobile = False):
    return {
        "user": user,
        "url_name": url_name,
        "mobile": mobile,
    }
