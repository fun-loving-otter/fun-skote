from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

from authentication.utilities import AccessRequiredMixin
from main.models import DataUpload
from main.forms.control import data as data_forms


class DataUploadListView(AccessRequiredMixin, ListView):
    model = DataUpload
    template_name = 'main/control/data/data_upload_table.html'



class DataUploadCreateView(AccessRequiredMixin, CreateView):
    model = DataUpload
    form_class = data_forms.DataUploadForm
    template_name = 'control/form.html'
    success_url = reverse_lazy('control_panel:data-uploads')
