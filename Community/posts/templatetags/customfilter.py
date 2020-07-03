from django import template
from random import randint

register = template.Library()


@register.filter
def type(value):
    return value.__class__.__name__


@register.filter
def random(val):
    return randint(20, 1512)


@register.filter
def sub(val):
    return val - 1

@register.filter
def sub1(val):
    return val - 3

@register.filter
def first_name(val):
    name = str(val.split(" ")[0])
    return name