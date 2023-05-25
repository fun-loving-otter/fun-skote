from django.views.generic import TemplateView
from rest_framework.generics import ListAPIView

from main.models import Data
from main.serializers import DataSerializer


class DataTemplateView(TemplateView):
    template_name = 'main/data/data_table.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        exclude = {'id', 'uploaded_data_file'}
        context['model_fields'] = [field for field in Data._meta.get_fields() if field.name not in exclude]

        return context



class DataAPIListView(ListAPIView):
    queryset = Data.objects.all()
    serializer_class = DataSerializer
