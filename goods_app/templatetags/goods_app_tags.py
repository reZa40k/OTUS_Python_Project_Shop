from django import template
from goods_app.models import Categories

register = template.Library()


@register.simple_tag()
def categories_tag():
    return Categories.objects.all()
