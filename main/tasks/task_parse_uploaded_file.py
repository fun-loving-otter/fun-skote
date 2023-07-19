from celery import shared_task

from main.models import UploadedDataFile
from .parser_zip import ZipParser
from .parser_csv import CSVParser


@shared_task(bind=True)
def parse_uploaded_file(self, uploaded_data_file_id):
    uploaded_data_file = UploadedDataFile.objects.get(id=uploaded_data_file_id)

    path = uploaded_data_file.file.path

    if path.endswith('.zip'):
        parser = ZipParser(uploaded_data_file)
    elif path.endswith('.csv'):
        parser = CSVParser(uploaded_data_file)

    return parser.run(self)
