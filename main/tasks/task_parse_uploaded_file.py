from celery import shared_task

from main.tasks.parse_csv_file import parse_csv_file
from main.tasks.parse_zip_jsons import parse_zip_with_jsons
from main.models import UploadedDataFile


@shared_task
def parse_uploaded_file(uploaded_data_file_id):
    uploaded_data_file = UploadedDataFile.objects.get(id=uploaded_data_file_id)

    path = uploaded_data_file.file.path

    if path.endswith('.zip'):
        return parse_zip_with_jsons(uploaded_data_file)
    elif path.endswith('.csv'):
        return parse_csv_file(uploaded_data_file)
