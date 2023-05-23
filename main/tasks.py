import csv
from celery import shared_task

from main.models import Data, UploadedDataFile


def parse_csv_file(uploaded_data_file_id):
    uploaded_data_file = UploadedDataFile.objects.get(id=uploaded_data_file_id)
    csv_file = open(uploaded_data_file.file.path, 'r')
    reader = csv.reader(csv_file)

    headers = next(reader)  # Get the header row

    for row in reader:
        kwargs = {header: None for header in headers}

        for index, header in enumerate(headers):
            kwargs[header] = row[index]

        Data.objects.create(
            uploaded_data_file=uploaded_data_file,
            **kwargs
        )

    csv_file.close()

    # Optional: Mark the UploadedDataFile as processed
    uploaded_data_file.processed = True
    uploaded_data_file.save()
