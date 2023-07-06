from django.urls import path

from control_panel.views import generic_views, app_views, index_views
from authentication import urls_admin as auth_urls
from translations import urls_admin as lurls
from payments import urls_admin as purls
from core import urls_admin as curls
from main import urls_admin as murls
from affiliates import urls_admin as aurls
from emails import urls_admin as emails_urls


app_name = 'control_panel'
urlpatterns = [
    # Index
    path('', index_views.IndexView.as_view(), name='index'),

    # APP
    path('tracking', app_views.TrackingView.as_view(), name='tracking'),
    path('utm', app_views.UTMView.as_view(), name='utm'),

    # Generic
    path('files', generic_views.FilesView.as_view(), name='files'),
    path('file-edit', generic_views.FileEditView.as_view(), name='file-edit'),
]

urlpatterns += lurls.urlpatterns
urlpatterns += purls.urlpatterns
urlpatterns += curls.urlpatterns
urlpatterns += murls.urlpatterns
urlpatterns += aurls.urlpatterns
urlpatterns += auth_urls.urlpatterns
urlpatterns += emails_urls.urlpatterns
