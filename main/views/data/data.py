from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import ListAPIView

from main.models import Data, DataList
from main.rest.serializers import DataSerializer


class DataTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'main/data/data_table.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        fields = Data._header_field_mapping.values()
        context['model_fields'] = [Data._meta.get_field(field) for field in fields]

        # Get DataList objects where creator is the current user
        user = self.request.user
        context['datalists'] = DataList.objects.filter(creator=user)

        return context



class DataAPIListView(ListAPIView):
    queryset = Data.objects.all()
    serializer_class = DataSerializer
