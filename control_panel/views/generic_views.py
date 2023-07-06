from django.views.generic import TemplateView
from django.contrib import messages

from authentication.mixins import AccessRequiredMixin



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
