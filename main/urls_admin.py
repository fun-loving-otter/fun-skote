from django.urls import path

from main.views.control import data_export
from main.views.control import data_upload
from main.views.control import package_benefits


urlpatterns = [
    # Data Export
    path('data/export', data_export.DataExportTemplateView.as_view(), name='data-export'),
    path('api/data/start-export-csv', data_export.StartDataExportCSVAPIView.as_view(), name='api-data-export-csv'),
    # Data Upload
    path('data_uploads/', data_upload.DataUploadListView.as_view(), name='data-uploads'),
    path('data_uploads/create', data_upload.DataUploadCreateView.as_view(), name='data-upload-create'),
    path('data_uploads/new-file', data_upload.DataUploadDropzoneView.as_view(), name='data-upload-new-file'),
    # Package benefits
    path('package-benefits/', package_benefits.PackageWithBenefitsListView.as_view(), name='package-benefits'),
    path('package/<package_pk>/benefits/edit', package_benefits.PackageBenefitsUpdateView.as_view(), name='package-benefits-edit')
]
