from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.urls import reverse
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response

from authentication.mixins import AccessRequiredMixin
from main.models import DataExport
from main.filters.data import ExportDataFilter
from main.tasks import export_data_to_csv



class DataExportTemplateView(AccessRequiredMixin, ListView):
    template_name = 'main/control/data/data_export.html'
    model = DataExport

    def get_context_data(self):
        context = super().get_context_data()
        context['filter'] = ExportDataFilter()
        return context



# TODO: write tests for this
class StartDataExportCSVAPIView(AccessRequiredMixin, APIView):
    def post(self, request):
        # Get the filter parameters from the request POST parameters
        filter_params = request.POST.dict()

        # Call the Celery task asynchronously
        task_result = export_data_to_csv.delay(filter_params)

        data = {
            "task_id": task_result.task_id,
            "progress_url": reverse('control_panel:celery_progress:task_status', kwargs={'task_id': task_result.task_id})
        }
        return Response(data)
