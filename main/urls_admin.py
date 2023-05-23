from django.urls import path

from .views.control import data


urlpatterns = [
    path('data_uploads/', data.DataUploadListView.as_view(), name='data-uploads'),
    path('data_uploads/create', data.DataUploadCreateView.as_view(), name='data-upload-create'),
]
