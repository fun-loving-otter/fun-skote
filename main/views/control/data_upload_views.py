from django.views.generic import CreateView, ListView
from django.views.generic.edit import ProcessFormView, FormMixin
from django.urls import reverse_lazy
from django.http import JsonResponse

from control_panel.mixins import AccessRequiredMixin
from main.models import DataUpload, UploadedDataFile
from main.forms.control import data as data_forms


class DataUploadListView(AccessRequiredMixin, FormMixin, ListView):
    model = DataUpload
    form_class = data_forms.DataUploadForm
    template_name = 'main/control/data/data_upload_table.html'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('uploadeddatafile_set')


    def get_context_data(self, **kwargs):
        kwargs['form'] = self.get_form()
        return super().get_context_data(**kwargs)


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs



class DataUploadCreateView(AccessRequiredMixin, CreateView):
    template_name = 'main/control/data/data_upload_create.html'
    form_class = data_forms.DataUploadForm
    success_url = reverse_lazy('control_panel:data-uploads')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs



class DataUploadDropzoneView(AccessRequiredMixin, FormMixin, ProcessFormView):
    http_method_names = ['post']
    form_class = data_forms.DropzoneFileUploadForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


    def form_valid(self, form):
        is_last_chunk = form.save()
        if is_last_chunk:
            data = {
                'message': 'File uploaded successfully',
                'tmp_file_name': UploadedDataFile.get_file_name(
                    form.cleaned_data['file'],
                    form.cleaned_data['dzuuid']
                )
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'message': 'Chunk uploaded successfully'})


    def form_invalid(self, form):
        return JsonResponse({'errors': form.errors}, status=400)
