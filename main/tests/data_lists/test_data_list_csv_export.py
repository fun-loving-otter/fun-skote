import csv
import pytest

from django.urls import reverse

from core.tests.conftest import ViewTestBase
from main.models import DataColumnVisibility


class TestExportDataListCSVView(ViewTestBase):
    url_name = 'main:datalist-export-csv'

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
        assert response['Content-Type'] == 'text/csv'
        assert response['Content-Disposition'] == f'attachment; filename="{data_list}.csv"'

        # Parse the CSV content from the response
        csv_content = response.content.decode('utf-8')
        csv_reader = csv.reader(csv_content.splitlines())

        # Assert the CSV headers and data
        expected_headers = DataColumnVisibility.get_visible_headers()
        assert next(csv_reader) == expected_headers


    def test_subscribed_user_unowned_list_export_fails(self, url, auto_login_user):
        client, user = auto_login_user()

        response = client.get(url)

        assert response.status_code == 404
