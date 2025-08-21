from django import template

register = template.Library()

@register.filter
def hhmm(value):
    if not value:
        return ""
    total_seconds = int(value.total_seconds())
    hours, rem = divmod(total_seconds, 3600)
    minutes, _ = divmod(rem, 60)
    return f"{hours}h {minutes:02d}m"