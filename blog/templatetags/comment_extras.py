import hashlib
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()
@register.filter
@stringfilter
def hash(email):
    # hash the email address for privacy
    return hashlib.md5(email.encode("utf-8").lower().strip()).hexdigest()