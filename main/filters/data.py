from django_filters import rest_framework as filters

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

    class Meta:
        model = Data
        fields = ['founded_date', 'last_funding_date', 'estimate_revenue', 'number_of_employees',
                  'total_funding_amount', 'total_equity_funding', 'ipo_date', 'money_raised_at_ipo', 'valuation_at_ipo']
