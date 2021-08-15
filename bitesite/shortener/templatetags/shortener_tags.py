from django import template

from shortener.models import Links

register = template.Library()

@register.simple_tag()
def get_links():
    return Links.objects.all()