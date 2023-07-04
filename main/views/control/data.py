import csv

from django.views.generic import ListView, CreateView, TemplateView
from django.views import View
from django.http import HttpResponse
from django.urls import reverse_lazy

from authentication.mixins import AccessRequiredMixin
from main.models import DataUpload, Data
from main.forms.control import data as data_forms
from main.filters.data import ExportDataFilter


class DataUploadListView(AccessRequiredMixin, ListView):
    model = DataUpload
    template_name = 'main/control/data/data_upload_table.html'



class DataUploadCreateView(AccessRequiredMixin, CreateView):
    model = DataUpload
    form_class = data_forms.DataUploadForm
    template_name = 'control/form.html'
    success_url = reverse_lazy('control_panel:data-uploads')



class DataExportTemplateView(AccessRequiredMixin, TemplateView):
    template_name = 'main/control/data/data_export.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['filter'] = ExportDataFilter()
        return context



class DataExportCSVView(AccessRequiredMixin, View):
    def get(self, request):
        # Get the filter parameters from the request GET parameters
        filter_params = request.GET.dict()

        # Create the data filter instance
        data_filter = ExportDataFilter(filter_params, queryset=Data.objects.all())

        # Apply the filters to the queryset
        filtered_data = data_filter.qs

        # Prepare the CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="data_export.csv"'

        # Create the CSV writer
        writer = csv.writer(response)

        # Filter out header mapping to follow merged (2) (1) format
        header_mapping = Data._header_field_mapping
        for key in list(header_mapping.keys()):
            if any(x in key for x in ['CEO ', 'CFO ', 'CMO ']):
                del header_mapping[key]

        # Write the header row
        header_row = list(header_mapping.keys())
        writer.writerow(header_row)

        # Write the data rows
        for data_object in filtered_data:
            data_row = [getattr(data_object, field_name) for field_name in header_mapping.values()]
            writer.writerow(data_row)

        return response
