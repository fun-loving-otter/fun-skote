from importlib import import_module

from django.urls import path
from django.conf import settings

from control_panel.views import generic_views, index_views


app_name = 'control_panel'
urlpatterns = [
    # Index
    path('', index_views.IndexView.as_view(), name='index'),

    # Generic
    path('files', generic_views.FilesView.as_view(), name='files'),
    path('file-edit', generic_views.FileEditView.as_view(), name='file-edit'),
]


for app in settings.INSTALLED_APPS:
    try:
        _module = import_module(app + '.urls_admin')
        urlpatterns += _module.urlpatterns
    except ModuleNotFoundError:
        continue
