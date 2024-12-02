from __future__ import absolute_import
from django import template

register = template.Library()


def alaviiva_pois(value):
    return value.replace("_", " ")


register.filter("alaviiva_pois", alaviiva_pois)
