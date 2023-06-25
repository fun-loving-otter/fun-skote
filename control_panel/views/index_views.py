from django.views.generic import TemplateView
from django.contrib.auth import get_user_model

from authentication.mixins import AccessRequiredMixin

User = get_user_model()



class IndexView(AccessRequiredMixin, TemplateView):
	template_name = 'control/index.html'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)

		users_count = User.objects.count()
		if users_count:
			users = {
				"total": users_count,
			}
			context['users'] = users

		return context
