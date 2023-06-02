from django.views.generic import TemplateView
from rest_framework.generics import ListAPIView

from main.models import Data, DataList
from main.rest.serializers import DataSerializer
from main.mixins import DataPackageRequiredMixin
from main.rest.permissions import HasDataPackagePermission


class DataTemplateView(DataPackageRequiredMixin, TemplateView):
    template_name = 'main/data/data_table.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add Data fields to context
        fields = Data._header_field_mapping.values()
        context['model_fields'] = [Data._meta.get_field(field) for field in fields]

        context['hidden_fields'] = Data._hidden_fields

        # Get DataList objects where creator is the current user
        user = self.request.user
        context['datalists'] = DataList.objects.filter(creator=user)

        return context



class DataAPIListView(ListAPIView):
    queryset = Data.objects.all()
    serializer_class = DataSerializer
    permission_classes = [HasDataPackagePermission]

    def get_serializer(self, *args, **kwargs):
        kwargs['hide_fields'] = True

        return self.get_serializer_class()(*args, **kwargs)
