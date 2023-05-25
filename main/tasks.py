import csv
from celery import shared_task

from main.models import Data, UploadedDataFile


def count_lines(filename):
    line_count = 0
    with open(filename, 'r') as file:
        for _ in file:
            line_count += 1
    return line_count


@shared_task
def parse_csv_file(uploaded_data_file_id):
    uploaded_data_file = UploadedDataFile.objects.get(id=uploaded_data_file_id)

    rows_amount = count_lines(uploaded_data_file.file.path)

    csv_file = open(uploaded_data_file.file.path, 'r')
    reader = csv.reader(csv_file)

    headers = next(reader)  # Get the header row
    headers = [x for x in headers if x]

    uploaded_data_file.data_upload.number_of_rows = rows_amount
    uploaded_data_file.data_upload.number_of_columns = len(headers)
    uploaded_data_file.data_upload.save()

    data_objects = []
    for row in reader:
        kwargs = {}

        for index, header in enumerate(headers):
            field = Data._header_field_mapping.get(header.strip())
            if field is None or row[index] in ['-', '—']:
                continue

            kwargs[field] = row[index]

        data_objects.append(Data(
            uploaded_data_file=uploaded_data_file,
            **kwargs
        ))

    Data.objects.bulk_create(data_objects)

    csv_file.close()

    uploaded_data_file.processed = True
    uploaded_data_file.save()
