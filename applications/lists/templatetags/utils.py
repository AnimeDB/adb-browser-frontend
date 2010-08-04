from coffin import template
register = template.Library()

def absolute_url(arg):
    return arg.get_absolute_url()

register.filter('url', absolute_url)