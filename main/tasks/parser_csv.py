import csv
import json
import logging
import dateparser

from io import StringIO
from datetime import datetime
from celery_progress.backend import ProgressRecorder

from django.db.models import DateField, F
from django.utils import timezone

from main.models import Data



logger = logging.getLogger(__name__)

class CSVParser:
    def __init__(self, uploaded_data_file):
        self.uploaded_data_file = uploaded_data_file
        self.filepath = uploaded_data_file.file.path
        self.rows_processed = 0
        self.data_objects_created = 0
        self.total_rows = 0

        self.dateparse_settings = {'RELATIVE_BASE': datetime.fromtimestamp(0)}



    def run(self, task):
        self.task = task
        self.progress_recorder = ProgressRecorder(task)

        logger.info(f"Started processing {self.uploaded_data_file} in csv mode")

        self.parse_csv()

        # Mark file as processed
        self.uploaded_data_file.processed = True
        self.uploaded_data_file.save()

        logger.info(f'Finished processing {self.uploaded_data_file}. {self.data_objects_created} objects created.')

        # Generate result
        result = {
            "rows": self.total_rows,
            "rows_processed": self.rows_processed,
            "data_objects_created": self.data_objects_created
        }
        return json.dumps(result)


    def load_content(self):
        with open(self.filepath, 'r') as file:
            csv_content = file.read().strip()

        self.total_lines = csv_content.count('\n') + 1
        self.total_rows = self.total_lines - 1

        return csv_content


    def parse_csv(self):
        # Read file into memory
        content = self.load_content()

        csv_file = StringIO(content)
        reader = csv.reader(csv_file)

        headers = next(reader)  # Get the header row
        headers = [x for x in headers if x]

        # Update stats
        self.uploaded_data_file.data_upload.number_of_rows += F('number_of_rows') + self.total_rows
        self.uploaded_data_file.data_upload.number_of_columns = len(headers)
        self.uploaded_data_file.data_upload.save()

        # Create Data objects for rows
        data_objects = []
        for row in reader:
            data_objects.append(self.parse_row(row, headers))
            self.rows_processed += 1
            self.progress_recorder.set_progress(self.rows_processed, self.total_rows)

        csv_file.close()
        Data.objects.bulk_create(data_objects)
        self.data_objects_created += len(data_objects)



    def parse_row(self, row, headers):
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

        obj = Data(
            uploaded_data_file=self.uploaded_data_file,
            **kwargs
        )
        return obj
