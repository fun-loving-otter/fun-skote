from django.urls import path

from main.views.control import data
from main.views.control import package_benefits


urlpatterns = [
    # Data
    path('data/export', data.DataExportTemplateView.as_view(), name='data-export'),
    path('data/export-csv', data.DataExportCSVView.as_view(), name='data-export-csv'),
    # DataUpload
    path('data_uploads/', data.DataUploadListView.as_view(), name='data-uploads'),
    path('data_uploads/create', data.DataUploadCreateView.as_view(), name='data-upload-create'),
    # Package benefits
    path('package-benefits/', package_benefits.PackageWithBenefitsListView.as_view(), name='package-benefits'),
    path('package/<package_pk>/benefits/edit', package_benefits.PackageBenefitsUpdateView.as_view(), name='package-benefits-edit')
]
