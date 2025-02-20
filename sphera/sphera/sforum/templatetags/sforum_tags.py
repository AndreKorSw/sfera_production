from django import template
from sforum.models import *
register=template.Library()



# @register.inclusion_tag("xforum/list_categories.html")
@register.inclusion_tag('sforum/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats=Categories.objects.all()
    else:
        cats=Categories.objects.order_by(sort)
    return {"cats":cats,"cat_selected":cat_selected}

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
