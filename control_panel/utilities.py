from django.conf import settings


class VirtualHostMiddleware:
	virtual_hosts = {
		settings.CONTROL_PANEL_DOMAIN: "control_panel.urls_standalone",
		settings.DOMAIN: settings.ROOT_URLCONF,
	}

	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		host = request.get_host()

		if not settings.DEBUG:
			request.urlconf = self.virtual_hosts.get(host)

		response = self.get_response(request)
		return response
