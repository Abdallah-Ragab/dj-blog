from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()
@register.filter
@stringfilter
def read_time(post_body):
    words_per_minute = 150
    words = len(post_body.split())
    minutes = words / words_per_minute
    read_time = round(minutes)
    return read_time

# make a custom filter to get the current url and add query params to it
@register.simple_tag(takes_context=True)
def url_append_query_params(context, **kwargs):
    url = context["request"].get_full_path()
    if "?" in url:
        url += "&"
    else:
        url += "?"
    for key, value in kwargs.items():
        # if the param is the last one in the url, don't add the & at the end
        if key == list(kwargs.keys())[-1]:
            url += f"{key}={value}"
        else:
            url += f"{key}={value}&"
    return url