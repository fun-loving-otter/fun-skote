import pytest
import os

from uuid import uuid4

from django.core.files.base import ContentFile

from main.models import DataUpload, UploadedDataFile
from authentication.tests.conftest import AdminTemplateViewTestBase
from core.tests.conftest import ViewTestBase


class TestDataUploadCreateView(AdminTemplateViewTestBase):
    url_name = 'control_panel:data-upload-create'

    def test_get_succeeds(self, url, admin_client):
        response = admin_client.get(url)
        assert response.status_code == 200
        assert 'form' in response.context


    def test_post_creation_succeeds(self, url, admin_user, admin_client, data_sample_csv_file, data_sample_zip_file):
        # Save file content in the temporary directory
        csv_filename = f'{uuid4()}.csv'
        csv_file_path = UploadedDataFile.get_upload_temp_dir(admin_user) / csv_filename
        with open(csv_file_path, 'wb') as csv_file:
            csv_file.write(data_sample_csv_file.read())

        zip_filename = f'{uuid4()}.zip'
        zip_file_path = UploadedDataFile.get_upload_temp_dir(admin_user) / zip_filename
        with open(zip_file_path, 'wb') as zip_file:
            zip_file.write(data_sample_zip_file.read())

        # Prepare the data for the request
        data = {
            'name': 'Test Data Upload',
            'files': f'{csv_filename},{zip_filename}'
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



@pytest.mark.urls('control_panel.urls_standalone')
class TestDataUploadDropzoneView(ViewTestBase):
    url_name = 'control_panel:data-upload-new-file'
    method = 'POST'

    def test_post_chunked_upload_creates_tmp_file(self, url, admin_user, admin_client, data_sample_csv_file):
        # Simulate the file upload in two chunks
        filename = data_sample_csv_file.name
        first_chunk = ContentFile(data_sample_csv_file.read(1024), name=filename)  # Read the first chunk
        second_chunk = ContentFile(data_sample_csv_file.read(), name=filename)  # Read the second chunk
        upload_id = uuid4()

        # Prepare the data for the request
        data = {
            'file': first_chunk,
            'dzuuid': upload_id,
            'dztotalchunkcount': 2,
            'dzchunkindex': 0,
        }

        # Make the first chunk upload request
        response = admin_client.post(url, data, format='multipart')

        # Assert the response status code and message
        assert response.status_code == 200
        assert response.json() == {'message': 'Chunk uploaded successfully'}
        # Assert that the first chunk is saved in the temporary directory
        tmp_chunk_path = UploadedDataFile.get_upload_temp_dir(admin_user) / UploadedDataFile.get_chunk_name(first_chunk, upload_id, 0)
        assert os.path.exists(tmp_chunk_path) is True

        # Prepare the data for the second chunk upload request
        data = {
            'file': second_chunk,
            'dzuuid': upload_id,
            'dztotalchunkcount': 2,
            'dzchunkindex': 1,
        }

        # Make the second chunk upload request
        response = admin_client.post(url, data, format='multipart')

        # Assert the response status code and message
        assert response.status_code == 200
        assert response.json() == {
            'message': 'File uploaded successfully',
            'tmp_file_name': UploadedDataFile.get_file_name(second_chunk, upload_id)
        }

        # Assert that the temporary file was created
        tmp_file_path = UploadedDataFile.get_upload_temp_dir(admin_user) / UploadedDataFile.get_file_name(second_chunk, upload_id)
        assert os.path.exists(tmp_file_path) is True

        # Cleanup
        os.remove(tmp_file_path)
