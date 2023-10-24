from django import template

register = template.Library()


@register.filter(name='add_css')
def add_css(field, arg):
    css_classes = field.field.widget.attrs.get('class', '')

    if css_classes:
        css_classes = css_classes.split(' ')
    else:
        css_classes = []

    args = arg.split(' ')
    for a in args:
        if a not in css_classes:
            css_classes.append(a)

    return field.as_widget(attrs={'class': ' '.join(css_classes)})
