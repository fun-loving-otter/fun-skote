import os
import pytest

from main.models import DataUpload, UploadedDataFile
from main.tasks.parse_zip_jsons import parse_zip_with_jsons


@pytest.mark.django_db
def test_csv_parser_creates_data_objects(data_sample_zip_file):
    data_upload = DataUpload.objects.create(name="Test Upload")

    uploaded_data_file = UploadedDataFile.objects.create(
        data_upload=data_upload,
        file=data_sample_zip_file
    )

    parse_zip_with_jsons(uploaded_data_file)

    data_upload.refresh_from_db()
    assert data_upload.number_of_rows > 0
    assert data_upload.number_of_columns == 0

    uploaded_data_file.refresh_from_db()
    assert uploaded_data_file.processed is True
    assert uploaded_data_file.data_set.count() == data_upload.number_of_rows

    os.remove(uploaded_data_file.file.path)
