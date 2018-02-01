from django import template
from django.db.models import Count
from random import randint

register = template.Library()

@register.filter
def random_objects(value, arg): # Only one argument.
    count = arg.aggregate(count=Count('id'))['count']
    random_index = randint(0, count - 1)
    return arg.all()[random_index]
