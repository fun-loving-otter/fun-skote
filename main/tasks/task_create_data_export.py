import csv

from itertools import islice

from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.utils import timezone

from celery import shared_task
from celery_progress.backend import ProgressRecorder

from main.filters.data import ExportDataFilter
from main.models import Data, DataExport


# TODO: write tests for this
@shared_task(bind=True)
def export_data_to_csv(self, filter_params):
    progress_recorder = ProgressRecorder(self)

    # Prepare the CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data_export.csv"'

    # Create the CSV writer
    writer = csv.writer(response)

    # Filter out header mapping to follow merged (2) (1) format
    header_mapping = Data._header_field_mapping
    for key in list(header_mapping.keys()):
        if any(x in key for x in ['CEO ', 'CFO ', 'CMO ']):
            del header_mapping[key]

    # Create the data filter instance
    data_filter = ExportDataFilter(filter_params, queryset=Data.objects.all())

    # Apply the filters to the queryset
    filtered_data = data_filter.qs

    # Write the header row
    header_row = list(header_mapping.keys())
    writer.writerow(header_row)

    # Initialize progress
    total_rows = filtered_data.count()
    processed_rows = 0

    # Write the data rows
    # Split the filtered_data into chunks of 1000 and process each chunk
    chunk_size = 1000
    for chunk in (islice(filtered_data, i, i + chunk_size) for i in range(0, filtered_data.count(), chunk_size)):
        for data_object in chunk:
            data_row = [getattr(data_object, field_name) for field_name in header_mapping.values()]
            writer.writerow(data_row)

            # Update progress
            processed_rows += 1
        progress_recorder.set_progress(processed_rows, total_rows)

    # Save export to history
    data_export = DataExport.objects.create(
        file=ContentFile(response.content, name=f'data_export{timezone.now()}.csv'),
        info=str(dict(filter_params))
    )

    # Return the filename of the exported CSV file
    return data_export.file.url
