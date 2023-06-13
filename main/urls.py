from django.urls import path

from main.views.data import data as data_views
from main.views.data import datalist as datalist_views
from main.views.package import package as package_views


app_name = 'main'


urlpatterns = [
    # Data
    path('api/data-list', data_views.DataAPIListView.as_view(), name='api-data-list'),
    path('data/', data_views.DataTemplateView.as_view(), name='data-list'),
    # DataList
    path('datalists/', datalist_views.DataListListView.as_view(), name='datalist-list'),
    path('datalists/create/', datalist_views.DataListCreateView.as_view(), name='datalist-create'),
    path('datalist/<int:pk>/update', datalist_views.DataListUpdateAPIView.as_view(), name='api-datalist-update'),
    path('datalist/<int:pk>/destroy/', datalist_views.DataListDestroyAPIView.as_view(), name='api-datalist-destroy'),
    path('datalist/<int:pk>/export/csv', datalist_views.export_datalist_csv, name='datalist-export-csv'),
    path('datalist/<int:pk>/export/xls', datalist_views.export_datalist_xls, name='datalist-export-xls'),
    # Package
    path('package/select', package_views.PackageChoiceView.as_view(), name='buy-package')
]
