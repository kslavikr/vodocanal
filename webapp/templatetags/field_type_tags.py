from django import template


register = template.Library()

@register.filter
def field_type(ob):
    return ob.field.widget.__class__.__name__