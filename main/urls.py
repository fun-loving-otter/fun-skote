from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from main.views.data import data as data_views
from main.views.data import datalist as datalist_views


app_name = 'main'


urlpatterns = [
    path('api/data-list', data_views.DataAPIListView.as_view(), name='api-data-list'),
    path('', RedirectView.as_view(url=reverse_lazy('main:data-list')), name='index'),
    path('data/', data_views.DataTemplateView.as_view(), name='data-list'),
    path('datalists/', datalist_views.DataListListView.as_view(), name='datalist-list'),
    path('datalists/create/', datalist_views.DataListCreateView.as_view(), name='datalist-create'),
    path('datalist/<int:pk>/update', datalist_views.DataListUpdateAPIView.as_view(), name='api-datalist-update')
]
