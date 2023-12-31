from django.urls import path

from main.views.data import data as data_views
from main.views.data import datalist as datalist_views


app_name = 'main'

urlpatterns = [
    # Data
    path('api/data-list', data_views.DataAPIListView.as_view(), name='api-data-list'),
    path('data/', data_views.DataTemplateView.as_view(), name='data-list'),
    path('data2/', data_views.DataTemplateView2.as_view(), name='data-list2'),
    # DataList
    path('datalists/', datalist_views.DataListListView.as_view(), name='datalist-list'),
    path('datalists/create/', datalist_views.DataListCreateView.as_view(), name='datalist-create'),
    path('datalist/<int:pk>/export/csv', datalist_views.ExportCSVView.as_view(), name='datalist-export-csv'),
    path('datalist/<int:pk>/export/xls', datalist_views.ExportXLSView.as_view(), name='datalist-export-xls'),
    path('api/datalist/<int:pk>/update', datalist_views.DataListUpdateAPIView.as_view(), name='api-datalist-update'),
    path('api/datalist/<int:pk>/destroy/', datalist_views.DataListDestroyAPIView.as_view(), name='api-datalist-delete'),
]
