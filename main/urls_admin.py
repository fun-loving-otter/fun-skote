from django.urls import path

from main.views.control import data_export_views
from main.views.control import data_upload_views
from main.views.control import package_benefits_views
from main.views.control import data_column_views


urlpatterns = [
    # Data Export
    path('data/export', data_export_views.DataExportTemplateView.as_view(), name='data-export'),
    path('api/data/start-export-csv', data_export_views.StartDataExportCSVAPIView.as_view(), name='api-data-export-csv'),
    # Data Upload
    path('data-uploads/', data_upload_views.DataUploadListView.as_view(), name='data-uploads'),
    path('data-uploads/create', data_upload_views.DataUploadCreateView.as_view(), name='data-upload-create'),
    path('data-uploads/new-file', data_upload_views.DataUploadDropzoneView.as_view(), name='data-upload-new-file'),
    # Package benefits
    path('package-benefits/', package_benefits_views.PackageWithBenefitsListView.as_view(), name='package-benefits'),
    path('package/<package_pk>/benefits/edit', package_benefits_views.PackageBenefitsUpdateView.as_view(), name='package-benefits-edit'),
    # Data columns
    path('data-columns', data_column_views.DataColumnVisibilityListView.as_view(), name='data-columns'),
    path('api/data-column/<pk>/edit', data_column_views.DataColumnVisibilityUpdateAPIView.as_view(), name='api-data-column-edit')
]
