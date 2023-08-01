import csv

from io import StringIO

from control_panel.tests.conftest import AdminTemplateViewTestBase
from main.models import Data


class TestDataExportTemplateView(AdminTemplateViewTestBase):
    url_name = 'control_panel:data-export'

    def test_get_succeeds(self, url, admin_client, created_data):
        response = admin_client.get(url)

        assert response.status_code == 200
        assert 'filter' in response.context_data



# TODO
# class TestDataExportCSVView(AdminTemplateViewTestBase):
#     url_name = 'control_panel:data-export-csv'

#     def test_get_export_succeeds(self, url, admin_client, created_data):
#         response = admin_client.get(url)

#         # Assert the response status code and content type
#         assert response.status_code == 200
#         assert response['Content-Type'] == 'text/csv'

#         # Read the CSV content from the response
#         csv_content = response.content.decode('utf-8')
#         csv_reader = csv.reader(StringIO(csv_content))

#         # Assert the header row
#         header_row = next(csv_reader)
#         expected_header_row = list(Data._header_field_mapping.keys())
#         assert header_row == expected_header_row

#         # Assert the data rows
#         data_rows = list(csv_reader)
#         expected_data_rows = []
#         for data_object in Data.objects.all():
#             data_row = [str(getattr(data_object, field_name)) for field_name in Data._header_field_mapping.values()]
#             expected_data_rows.append(data_row)
#         assert data_rows == expected_data_rows
