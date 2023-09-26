from django import template
from decimal import *
register = template.Library()

@register.simple_tag()
def to_decimal(value, args):
    if(value and args):
        total = Decimal(value) * args
        print(total)
        return Decimal(total).quantize(Decimal('.01'), rounding=ROUND_UP)


@register.filter(name='times') 
def times(value):
    return range(value)
