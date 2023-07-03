import os
import pytest

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

    def test_get_succeeds(self, url, admin_client):
        response = admin_client.get(url)

        assert response.status_code == 200


    def test_post_creation_succeeds(self, url, admin_client, data_sample_csv_file, data_sample_zip_file):
        data = {
            'name': 'Test Data Upload',
            'files': [data_sample_csv_file, data_sample_zip_file]
        }

        response = admin_client.post(url, data=data, format='multipart', follow=True)

        assert response.status_code == 200

        # Check that the data upload was created and CSV file was processed
        data_upload = DataUpload.objects.first()
        assert data_upload is not None
        assert data_upload.name == 'Test Data Upload'
        assert data_upload.size_of_files == data_sample_csv_file.size + data_sample_zip_file.size
        assert data_upload.number_of_files == 2
        assert data_upload.number_of_rows > 0
        assert data_upload.number_of_columns > 0

        # Check that the uploaded data file was created and processed
        uploaded_data_files = UploadedDataFile.objects.all()

        assert uploaded_data_files.count() == 2
        assert all(file.data_upload == data_upload for file in uploaded_data_files)
        assert all(file.processed is True for file in uploaded_data_files)
        assert sum(file.data_set.count() for file in uploaded_data_files) == data_upload.number_of_rows


        # Cleanup
        for uploaded_file in uploaded_data_files:
            os.remove(uploaded_file.file.path)
