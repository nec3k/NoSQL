import datetime
from django import template

register = template.Library()

@register.filter(name="timestamp_to_datetime")
def timestamp_to_datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)
