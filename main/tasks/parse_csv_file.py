import csv
import logging
import dateparser

from datetime import datetime

from django.db.models import DateField
from django.utils import timezone

from main.models import Data



dateparse_settings = {'RELATIVE_BASE': datetime.fromtimestamp(0)}
logger = logging.getLogger(__name__)


def count_lines(filename):
    line_count = 0
    with open(filename, 'r') as file:
        for _ in file:
            line_count += 1
    return line_count


def parse_csv_file(uploaded_data_file):
    logger.info(f"Started processing {uploaded_data_file} in csv mode")

    rows_amount = count_lines(uploaded_data_file.file.path)

    csv_file = open(uploaded_data_file.file.path, 'r')
    reader = csv.reader(csv_file)

    headers = next(reader)  # Get the header row
    headers = [x for x in headers if x]

    uploaded_data_file.data_upload.number_of_rows += rows_amount - 1
    uploaded_data_file.data_upload.number_of_columns = len(headers)
    uploaded_data_file.data_upload.save()

    data_objects = []
    for row in reader:
        kwargs = {}

        for index, header in enumerate(headers):
            # Get field name
            field_name = Data._header_field_mapping.get(header.strip())
            if field_name is None:
                continue

            value = row[index]

            # Get field and check if data needs to be processed
            field = Data._meta.get_field(field_name)
            if isinstance(field, DateField):
                value = dateparser.parse(value)
                if value is not None:
                    value = timezone.make_aware(value)

            kwargs[field_name] = value

        data_objects.append(Data(
            uploaded_data_file=uploaded_data_file,
            **kwargs
        ))

    Data.objects.bulk_create(data_objects)

    csv_file.close()

    uploaded_data_file.processed = True
    uploaded_data_file.save()

    logger.info(f"Finished processing {uploaded_data_file} in csv mode. {len(data_objects)} objects created.")

    return uploaded_data_file.id
