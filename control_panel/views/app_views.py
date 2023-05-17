from django.db.models import Count
from django.views.generic import TemplateView

from tracking import models as tm
from authentication.utilities import AccessRequiredMixin


class TrackingView(AccessRequiredMixin, TemplateView):
	template_name = 'control/tracking/tracking.html'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['cart_adds'] = tm.TrackedData.objects.filter(event='cart_add')
		context['registration_attempts'] = tm.TrackedData.objects.filter(event='registration_attempt')
		return context



class UTMView(AccessRequiredMixin, TemplateView):
	template_name = 'control/tracking/utm.html'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		q = tm.TrackedData.objects.exclude(utm_data={})
		context['events'] = [
			{
				'name': 'Visitors',
				'data': self.query_to_data(q.filter(event='utm_visit'))
			},
			{
				'name': 'Payments',
				'data': self.query_to_data(q.filter(event='payment'))
			},
			{
				'name': 'Checkout emails',
				'data': self.query_to_data(q.filter(event='registration_attempt'))
			}
		]
		return context

	def query_to_data(self, query):
		result = (
			query
			.values('utm_data')
			.annotate(utmcount=Count('utm_data'))
			.order_by()
		)

		# Reverse utm data to url
		for entry in result:
			data = entry['utm_data']
			parsed = '?'
			for i in data.items():
				parsed += f'{i[0]}={i[1]}&'
			entry['utm_data'] = parsed[:-1]
		return result
