from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from main.views.data import data as data_views


app_name = 'main'


urlpatterns = [
    path('api/data-list', data_views.DataAPIListView.as_view(), name='api-data-list'),
    path('', RedirectView.as_view(url=reverse_lazy('main:data-list')), name='index'),
    path('data/', data_views.DataTemplateView.as_view(), name='data-list'),
]
