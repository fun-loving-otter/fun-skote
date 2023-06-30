import os
import pytest

from django.core.files.uploadedfile import SimpleUploadedFile

from authentication.tests.conftest import AdminTemplateViewTestBase
from main.models import DataUpload, UploadedDataFile


class TestDataUploadListView(AdminTemplateViewTestBase):
    url_name = 'control_panel:data-uploads'

    @pytest.fixture
    def create_data_upload(self, db):
        def make_data_upload(**kwargs):
            return DataUpload.objects.create(**kwargs)
        return make_data_upload


    def test_get_succeeds(self, url, admin_client, create_data_upload):
        create_data_upload(name='File 1')
        create_data_upload(name='File 2')

        response = admin_client.get(url)

        assert response.status_code == 200
        assert len(response.context_data['object_list']) == 2



class TestDataUploadCreateView(AdminTemplateViewTestBase):
    url_name = 'control_panel:data-upload-create'

    @pytest.fixture
    def csv_file_path(self):
        return 'main/tests/control/sample_data/data_test.csv'


    def test_get_succeeds(self, url, admin_client):
        response = admin_client.get(url)

        assert response.status_code == 200


    def test_post_creation_succeeds(self, url, admin_client, csv_file_path):
        # Load the test csv file
        with open(csv_file_path, 'rb') as file:
            csv_file = SimpleUploadedFile(file.name, file.read())

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
        assert data_upload.size_of_files == csv_file.size
        assert data_upload.number_of_files == 1
        assert data_upload.number_of_rows > 0
        assert data_upload.number_of_columns > 0

        # Check that the uploaded data file was created and processed
        uploaded_data_file = UploadedDataFile.objects.first()
        assert uploaded_data_file is not None
        assert uploaded_data_file.data_upload == data_upload
        assert uploaded_data_file.processed is True

        assert uploaded_data_file.data_set.count() == data_upload.number_of_rows - 1

        # Cleanup
        os.remove(uploaded_data_file.file.path)
