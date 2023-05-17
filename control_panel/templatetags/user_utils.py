from django import template

register = template.Library()

@register.simple_tag
def get_available_pages(user):
	return [x.name for x in user.available_pages.all()]


@register.simple_tag
def check_permission(user, all_pages, *desired_pages):
	'''
	Returns True if at least one of desired pages can be accessed
	Or if user is superuser
	'''
	if user.is_superuser:
		return True
	else:
		available_pages = set(desired_pages).intersection(set(all_pages))
		can_access = len(available_pages) > 0
		return can_access
