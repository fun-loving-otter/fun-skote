from django.core.management.base import BaseCommand

from main.models import DataColumnVisibility, Data


# TODO: write tests for this
class Command(BaseCommand):
    help = 'Import DataColumnVisibility objects from HEADER_FIELD_MAPPING.'

    def handle(self, *args, **kwargs):
        new_columns = []
        # Loop through the keys in the HEADER_FIELD_MAPPING dictionary
        for header, field_name in Data._header_field_mapping.items():
            # Check if the DataColumnVisibility object already exists for the field_name
            if not DataColumnVisibility.objects.filter(field_name=field_name).exists():
                # Create a new DataColumnVisibility object for the field_name
                new_columns.append(DataColumnVisibility(field_name=field_name, header=header))
                # Log the created column name
                self.stdout.write(self.style.SUCCESS(f'Column added: {header}'))

        # Bulk create the new DataColumnVisibility objects
        DataColumnVisibility.objects.bulk_create(new_columns)

        # Log the number of new objects created
        num_created = len(new_columns)
        self.stdout.write(self.style.SUCCESS(f'{num_created} DataColumnVisibility objects imported successfully.'))
