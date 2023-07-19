import os
import json
import logging
import shutil

from zipfile import ZipFile
from collections import defaultdict
from celery_progress.backend import ProgressRecorder

from django.db.models import F

from main.models import Data
from .utilities import MagicGetter
from .mappings import FIELD_TO_JSON_MAPPING
from .json_processors import processors



logger = logging.getLogger(__name__)


class ZipParser:
    def __init__(self, uploaded_data_file):
        self.uploaded_data_file = uploaded_data_file
        self.zip_filepath = uploaded_data_file.file.path
        self.unzip_dir = os.path.splitext(self.zip_filepath)[0]  # /media/data.zip -> /media/data

        self.processed_files = 0
        self.successfully_parsed_files = 0
        self.data_objects_created = 0
        self.total_files = 0


    def run(self, task):
        self.task = task
        self.progress_recorder = ProgressRecorder(task)

        logger.info(f"Started processing {self.uploaded_data_file} in zip/json mode.")

        self.parse_zip()

        # Mark file as processed
        self.uploaded_data_file.processed = True
        self.uploaded_data_file.save()

        logger.info(f'Finished processing {self.uploaded_data_file}. {self.data_objects_created} objects created.')

        # Generate result
        result = {
            "processed_files": self.processed_files,
            "successfully_parsed_files": self.successfully_parsed_files,
            "data_objects_created": self.data_objects_created,
            "total_files": self.total_files
        }
        return json.dumps(result)


    def parse_zip(self):
        # Unzip the file
        with ZipFile(self.zip_filepath, 'r') as zip_ref:
            zip_ref.extractall(self.unzip_dir)
        files = self.find_files()

        # Call process function on each individual file
        for file in files['.json']:
            self.parse_json(file)
            self.processed_files += 1
            self.progress_recorder.set_progress(self.processed_files, self.total_files)

        # Clean up - remove the unzipped files
        shutil.rmtree(self.unzip_dir)


    def find_files(self):
        '''
        Returns dict with key=extension, val=[filepaths]
        '''
        discovered_files = defaultdict(list)
        # Walk through the unzipped directory
        for root, dirs, files in os.walk(self.unzip_dir):
            for file in files:
                filepath = os.path.join(root, file)
                ext = os.path.splitext(filepath)[1]
                discovered_files[ext].append(filepath)
                self.total_files += 1
        return discovered_files


    def parse_json(self, filepath):
        logger.info(f"Started processing {filepath} as part of the {self.uploaded_data_file} upload")
        try:
            with open(filepath) as json_file:
                data = json.load(json_file)
        except Exception as e:
            logger.error(f"ERROR: {e} while loading {filepath}.")
            return

        if not isinstance(data, dict):
            logger.error(f"ERROR: JSON file {filepath} had data type different than dict")
            return

        entries = data.get('entities', [])

        logger.info(f"Got {len(entries)} entries in {filepath}. Processing.")

        # Update stats
        self.uploaded_data_file.data_upload.number_of_rows = F('number_of_rows') + len(entries)
        self.uploaded_data_file.data_upload.save()

        # Create Data objects for entries
        data_objects = []
        for row in entries:
            data_objects.append(self.parse_row(row))

        Data.objects.bulk_create(data_objects)
        self.successfully_parsed_files += 1
        self.data_objects_created += len(data_objects)
        logger.info(f"Finished processing {filepath} in zip/json mode. {len(data_objects)} objects created.")


    def parse_row(self, row):
        row_getter = MagicGetter(row)
        kwargs = {}

        for field_name, keys in FIELD_TO_JSON_MAPPING.items():
            # Attempt to get value
            value = row_getter.get(keys)

            if value is None:
                continue

            # Apply processor to value
            processor = processors.get(field_name)
            value = processor(value)

            kwargs[field_name] = value

        obj = Data(
            uploaded_data_file=self.uploaded_data_file,
            **kwargs
        )
        return obj
