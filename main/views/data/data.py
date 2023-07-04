import json

from django.views.generic import TemplateView
from django.db import connection
from django.db.models import Max

from rest_framework.generics import ListAPIView
from django_countries import countries

from main.models import Data, DataList
from main.mixins import DataPackageRequiredMixin
from main.rest.serializers import DataSerializer
from main.rest.permissions import HasDataPackagePermission
from main.rest.paginators import CustomDatatablesPaginator
from main.rest.throttles import LimitedActionThrottle
from main.consts import action_names
from main.filters.data import DataFilter


class DataTemplateView(DataPackageRequiredMixin, TemplateView):
    template_name = 'main/data/data_table.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add Data fields to context
        fields = Data._header_field_mapping.values()

        context['model_fields'] = [Data._meta.get_field(field) for field in fields]
        context['hidden_fields'] = Data._hidden_fields
        context['searchable_fields'] = Data._searchable_fields

        # Get DataList objects where creator is the current user
        user = self.request.user
        context['datalists'] = DataList.objects.filter(creator=user)

        context['select_options'] = json.dumps({
            'headquarters': [country for code, country in list(countries)]
        })

        return context



class DataAPIListView(ListAPIView):
    action_name = action_names.ACTION
    serializer_class = DataSerializer
    permission_classes = [HasDataPackagePermission]
    throttle_classes = [LimitedActionThrottle]
    pagination_class = CustomDatatablesPaginator
    filterset_class = DataFilter

    def get_queryset(self):
        q = Data.objects.all()
        if connection.vendor == 'postgresql':
            q = q.order_by('-pk').distinct('organization_name')
        else:
            pks_q = q.values('organization_name').annotate(max_pk=Max('pk')).values('max_pk')
            q = q.filter(pk__in=pks_q)
        return q


    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


    def get_serializer(self, *args, **kwargs):
        kwargs['hide_fields'] = True

        return self.get_serializer_class()(*args, **kwargs)
