import csv

from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.utils import timezone

from authentication.mixins import AccessRequiredMixin
from main.models import Data, DataExport
from main.filters.data import ExportDataFilter



class DataExportTemplateView(AccessRequiredMixin, ListView):
    template_name = 'main/control/data/data_export.html'
    model = DataExport

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

        # Save export to history
        DataExport.objects.create(
            file=ContentFile(response.content, name=f'data_export{timezone.now()}.csv'),
            info=str(dict(request.GET))
        )
        return response



class DataExportRedownloadview(AccessRequiredMixin, SingleObjectMixin, View):
    model = DataExport

    def get(self, request, *args, **kwargs):
        # Retrieve the DataExport object
        data_export = self.get_object()

        # Open the file and read its content
        with data_export.file.open(mode='rb') as file:
            file_content = file.read()

        # Create an HttpResponse with the file content as the response body
        response = HttpResponse(file_content, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(data_export.file.name)

        return response
