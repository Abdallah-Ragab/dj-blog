from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()
@register.filter
@stringfilter
def read_time(post_body):
    words_per_minute = 200
    words = len(post_body.split())
    minutes = words / words_per_minute
    read_time = round(minutes)
    return read_time
