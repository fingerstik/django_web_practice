from datetime import timedelta

from django import template
from django.utils import timezone

register = template.Library()


@register.simple_tag
def created_string(post):
    date = post.date
    time = timezone.now() - date
    if time < timedelta(minutes=1):
        return 'just few time ago'
    elif time < timedelta(hours=1):
        return str(int(time.seconds / 60)) + 'min(s) ago'
    elif time < timedelta(days=1):
        return str(int(time.seconds / 3600)) + 'hour(s) ago'
    elif time < timedelta(days=7):
        return str(int(time.days)) + 'day(s) ago'
    else:
        return str(date.strftime('%Y. %m. %d'))

