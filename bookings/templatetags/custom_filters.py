from django import template

register = template.Library()

STATUS_CLASS_MAP = {
    'Pending': 'text-warning',
    'Confirmed': 'text-primary',
    'Completed': 'text-success',
    'Cancelled': 'text-danger',
}


@register.filter(name='status_class')
def status_class(status):
    return STATUS_CLASS_MAP.get(status, '')


@register.filter(name='add_class')
def add_class(field, css):
    return field.as_widget(attrs={"class": css})
