from django.views.generic import TemplateView
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError

from authentication.utilities import AccessRequiredMixin



class FilesView(AccessRequiredMixin, TemplateView):
	template_name = 'control/files/files.html'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		return context



class FileEditView(AccessRequiredMixin, TemplateView):
	template_name = 'control/files/file_edit.html'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		fname = self.request.GET.get('file')
		with open(fname, 'r') as f:
			content = f.read()
		context['file_name'] = fname
		context['file_content'] = content
		return context

	def post(self, request):
		fname = self.request.GET.get('file')
		new_content = self.request.POST.get('content')
		with open(fname, 'w') as f:
			f.write(new_content)
		messages.success(request, "File updated successfully")
		return self.get(request)



class EmailsView(AccessRequiredMixin, TemplateView):
	template_name = 'control/emails.html'

	def post(self, request):
		email = request.POST.get('email')
		email_files = [
			'authentication/emails/change_email.txt',
			'authentication/emails/mail_confirm.html',
			'authentication/emails/mail_confirm.txt',
			'authentication/emails/recoverpw_email.txt',
			'emails/order_created.txt',
			'emails/order_status_update.txt',
			'emails/checkout_reminder.txt'
		]

		from store.models import Order
		c = {
			"email": email,
			'domain': request.build_absolute_uri("/")[:-1],
			"uid": 'uid',
			"user": request.user,
			'token': 'token',
			'orders': Order.objects.all()[:5],
			'order': Order.objects.all()[0]
		}
		try:
			for i in email_files:
				email_text = render_to_string(i, c)
				# compat for html messages
				html_message = email_text if i.endswith('.html') else None
				send_mail(
					i.split('/')[-1],
					email_text,
					None,
					[email],
					fail_silently=False,
					html_message=html_message
				)
			messages.success(request, 'Emails sent')
		except BadHeaderError as e:
			print(f'Email testing error. Error: {e}')
			messages.error(request, "An error occured")
		return self.get(request)
