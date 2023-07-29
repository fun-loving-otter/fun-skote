from django_filters.rest_framework import DjangoFilterBackend
from django.db import connection
from django.db.models import Max


from main.rest.serializers import DataFiltersSerializer


class PostDataFilterBackend(DjangoFilterBackend):
    def get_filterset_kwargs(self, request, queryset, view):
        kwargs = super().get_filterset_kwargs(request, queryset, view)
        kwargs['data'] = dict(kwargs['data'])

        serializer = DataFiltersSerializer(data=request.data)

        if serializer.is_valid():
            filters = serializer.data['filters']
            kwargs['data'].update(filters)

        return kwargs


    def filter_queryset(self, request, queryset, view):
        queryset = super().filter_queryset(request, queryset, view)

        if connection.vendor == 'postgresql':
            queryset = queryset.order_by('organization_name', '-pk').distinct('organization_name')
        else:
            pks_queryset = queryset.values('organization_name').annotate(max_pk=Max('pk')).values('max_pk')
            queryset = queryset.filter(pk__in=pks_queryset)

        view._datatables_filtered_count = queryset.count()

        return queryset
