from django.urls import path

from main.views.control import data


urlpatterns = [
    # DataUpload
    path('data_uploads/', data.DataUploadListView.as_view(), name='data-uploads'),
    path('data_uploads/create', data.DataUploadCreateView.as_view(), name='data-upload-create'),
]
