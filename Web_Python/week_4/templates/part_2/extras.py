from django import template

register = template.Library()

@register.filter
def inc(val, incr):
    val = int(val)
    incr = int(incr)
    val += incr
    return val

@register.simple_tag
def division(a, b, to_int=False):
    if to_int:
        return int(int(a) / int(b))
    else:
        return int(a) / int(b)