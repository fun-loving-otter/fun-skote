from django.views.generic import TemplateView

from django_countries import countries
from django.db.models import OuterRef, Subquery, F

from rest_framework.generics import ListAPIView
from rest_framework_datatables.filters import DatatablesFilterBackend

from main.models import Data, DataList
from main.mixins import DataPackageRequiredMixin, DataPackageCheckerMixin
from main.rest.serializers import DataSerializer
from main.rest.paginators import CustomDatatablesPaginator
from main.rest.throttles import LimitedActionThrottle
from main.consts import action_names
from main.filters.data import DataFilter
from payments.rest.permissions.subscription import HasSubscriptionPermission
from main.filters.post_backend import PostDataFilterBackend


class DataTemplateView(DataPackageRequiredMixin, TemplateView):
    template_name = 'main/data/data_table.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add Data fields to context
        fields = Data._header_field_mapping.values()

        context['model_fields'] = [Data._meta.get_field(field) for field in fields]
        context['hidden_fields'] = Data._hidden_fields
        context['searchable_fields'] = {}
        for filter_type, field_names in Data._searchable_fields.items():
            context['searchable_fields'][filter_type] = [Data._meta.get_field(field) for field in field_names]

        # Get DataList objects where creator is the current user
        user = self.request.user
        context['datalists'] = DataList.objects.filter(creator=user)

        context['select_options'] = {
            'headquarters': [country for code, country in list(countries)]
        }

        return context



class DataTemplateView2(DataTemplateView):
    template_name = 'main/data/data_table2.html'


class DataAPIListView(DataPackageCheckerMixin, ListAPIView):
    action_name = action_names.ACTION
    serializer_class = DataSerializer
    permission_classes = [HasSubscriptionPermission]
    throttle_classes = [LimitedActionThrottle]
    pagination_class = CustomDatatablesPaginator
    filterset_class = DataFilter
    filter_backends = [DatatablesFilterBackend, PostDataFilterBackend]

    def get_queryset(self):
        queryset = Data.objects.all()

        latest_record_subquery = queryset.filter(
            organization_name=OuterRef('organization_name')
        ).order_by('-pk')

        queryset = queryset.annotate(
            is_latest_record=Subquery(latest_record_subquery.values('pk')[:1])
        ).filter(is_latest_record=F('pk'))

        return queryset


    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


    def get_serializer(self, *args, **kwargs):
        kwargs['hide_fields'] = True

        return self.get_serializer_class()(*args, **kwargs)
