from django import template
from authentication.models import AdminPage

register = template.Library()

@register.simple_tag
def get_available_admin_pages(user):
    '''
    Returns a dictionary where the keys are the page names
    and the values are booleans indicating whether the user has access.
    '''
    all_pages = set(x.replace('-', '_') for x in AdminPage.objects.values_list('name', flat=True))

    permissions = {}

    if user.is_superuser:
        for page in all_pages:
            permissions[page] = True
    else:
        available_pages = set(x.replace('-', '_') for x in user.available_pages.values_list('name', flat=True))
        for page in all_pages:
            permissions[page] = page in available_pages

    return permissions
