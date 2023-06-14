import pytest
import os

from django.urls import reverse, reverse_lazy
from django.test import override_settings
from django.core.files.uploadedfile import SimpleUploadedFile

from authentication.tests.conftest import check_template_view_access
from main.models import DataUpload, UploadedDataFile


@pytest.fixture
def create_data_upload(db):
    def make_data_upload(**kwargs):
        return DataUpload.objects.create(**kwargs)
    return make_data_upload



@pytest.fixture
def csv_file_path():
    return 'main/tests/control/data_test.csv'



@pytest.mark.django_db
@pytest.mark.urls('control_panel.urls_standalone')
@pytest.mark.parametrize(
    'url',
    [
        reverse_lazy('control_panel:data-uploads'),
        reverse_lazy('control_panel:data-upload-create'),
    ]
)
def test_template_view_access(url, auto_login_user, admin_client):
    check_template_view_access(url, auto_login_user, admin_client)




@pytest.mark.django_db
@pytest.mark.urls('control_panel.urls_standalone')
def test_data_upload_list_view(admin_client, create_data_upload):
    create_data_upload(name='File 1')
    create_data_upload(name='File 2')

    response = admin_client.get(reverse('control_panel:data-uploads'))

    assert response.status_code == 200
    assert len(response.context_data['object_list']) == 2




@pytest.mark.django_db
@pytest.mark.urls('control_panel.urls_standalone')
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)  # Ensure tasks are executed synchronously for testing
def test_data_upload_create_view(admin_client, csv_file_path):
    # Load the test csv file
    with open(csv_file_path, 'rb') as file:
        csv_file = SimpleUploadedFile(file.name, file.read())

    url = reverse('control_panel:data-upload-create')
    data = {
        'name': 'Test Data Upload',
        'csv_files': [csv_file]
    }

    response = admin_client.post(url, data=data, format='multipart', follow=True)

    assert response.status_code == 200

    # Check that the data upload was created and CSV file was processed
    data_upload = DataUpload.objects.first()
    assert data_upload is not None
    assert data_upload.name == 'Test Data Upload'
    assert data_upload.size_of_files > 0
    assert data_upload.number_of_files > 0
    assert data_upload.number_of_rows > 0
    assert data_upload.number_of_columns > 0

    # Check that the uploaded data file was created and processed
    uploaded_data_file = UploadedDataFile.objects.first()
    assert uploaded_data_file is not None
    assert uploaded_data_file.data_upload == data_upload
    assert uploaded_data_file.processed

    assert uploaded_data_file.data_set.count() == data_upload.number_of_rows - 1

    # Cleanup
    os.remove(uploaded_data_file.file.path)
