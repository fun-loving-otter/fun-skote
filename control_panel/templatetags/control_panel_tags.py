import json
import os
from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def get_sidebar_layout():
    sidebar_items = []

    for app in settings.INSTALLED_APPS:
        try:
            with open(os.path.join(settings.BASE_DIR, app, 'templates', 'sidebar_layout_control.json')) as f:
                items = json.load(f)
                sidebar_items.extend(items)
        except FileNotFoundError:
            continue

    return sidebar_items
