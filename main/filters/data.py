from django_filters import rest_framework as filters
from django.forms.widgets import DateInput

from main.models import Data


class DataFilter(filters.FilterSet):
    founded_date = filters.DateFromToRangeFilter()
    last_funding_date = filters.DateFromToRangeFilter()
    estimate_revenue = filters.NumberFilter(lookup_expr='range')
    number_of_employees = filters.NumberFilter(lookup_expr='range')
    total_funding_amount = filters.NumberFilter(lookup_expr='range')
    total_equity_funding = filters.NumberFilter(lookup_expr='range')
    ipo_date = filters.DateFromToRangeFilter()
    money_raised_at_ipo = filters.NumberFilter(lookup_expr='range')
    valuation_at_ipo = filters.NumberFilter(lookup_expr='range')
    headquarters = filters.CharFilter()

    class Meta:
        model = Data
        fields = ['founded_date', 'last_funding_date', 'estimate_revenue', 'number_of_employees',
                  'total_funding_amount', 'total_equity_funding', 'ipo_date', 'money_raised_at_ipo', 'valuation_at_ipo', 'headquarters']



class ExportDataFilter(filters.FilterSet):
    min_upload_date = filters.DateFilter(
        field_name='uploaded_data_file__data_upload__date',
        lookup_expr='gte',
        label="Uploaded after",
        widget=DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    min_last_funding_date = filters.DateFilter(
        field_name='last_funding_date',
        lookup_expr='gte',
        label="Last funding after",
        widget=DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    class Meta:
        model = Data
        fields = []
