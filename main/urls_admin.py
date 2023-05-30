from django.urls import path

from main.views.control import data
from main.views.control import package


urlpatterns = [
    # DataUpload
    path('data_uploads/', data.DataUploadListView.as_view(), name='data-uploads'),
    path('data_uploads/create', data.DataUploadCreateView.as_view(), name='data-upload-create'),
    # Package
    path('packages/', package.PackageListView.as_view(), name='packages'),
    path('packages/<int:pk>/update/', package.PackageUpdateView.as_view(), name='package-edit'),
    path('packages/create/', package.PackageCreateView.as_view(), name='package-create'),
    path('api/packages/<int:pk>/delete/', package.PackageDestroyAPIView.as_view(), name='api-package-delete'),
]
