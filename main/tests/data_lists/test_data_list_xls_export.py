import xlrd
import pytest

from django.urls import reverse

from core.tests.conftest import ViewTestBase
from main.models import DataColumnVisibility


class TestExportDataListXLSView(ViewTestBase):
    url_name = 'main:datalist-export-xls'

    @pytest.fixture
    def data_list(self, create_subscribed_user, create_data_list):
        self.client, self.user = create_subscribed_user(api=True)
        self.created_data_list = create_data_list(self.user)
        return self.created_data_list


    @pytest.fixture
    def url(self, data_list):
        return reverse(self.url_name, kwargs={'pk': data_list.pk})


    def test_subscribed_user_all_column_export_succeeds(self, url):
        self.verify_export(url)


    def test_subscribed_user_partial_column_export_succeeds(self, url):
        # Hide first 10 columns
        DataColumnVisibility.objects.filter(pk__lte=10).update(visible=False)
        self.verify_export(url)


    def verify_export(self, url):
        data_list = self.created_data_list

        response = self.client.get(url)

        # Assert the response
        assert response.status_code == 200
        assert response['Content-Type'] == 'application/ms-excel'
        assert response['Content-Disposition'] == f'attachment; filename="{data_list}.xls"'

        # Load the Excel content from the response
        xls_content = response.content
        xls_workbook = xlrd.open_workbook(file_contents=xls_content)
        xls_sheet = xls_workbook.sheet_by_index(0)

        # Assert the Excel headers and data
        expected_headers = DataColumnVisibility.get_visible_headers()
        excel_headers = [cell.value for cell in xls_sheet.row(0)]
        assert excel_headers == expected_headers


    def test_subscribed_user_unowned_list_export_fails(self, url, auto_login_user):
        client, user = auto_login_user()

        response = client.get(url)

        assert response.status_code == 404
