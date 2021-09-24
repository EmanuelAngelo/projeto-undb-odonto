from django import template
from django.conf import settings

register = template.Library()

@register.filter
def user_has_group(user, group):
    return user.groups.filter(name=group).exists() or user.is_superuser