import pytest

from control_panel.tests.conftest import AdminTemplateViewTestBase
from main.models import DataUpload


class TestDataUploadListView(AdminTemplateViewTestBase):
    url_name = 'control_panel:data-uploads'

    @pytest.fixture
    def create_data_upload(self, db):
        def make_data_upload(**kwargs):
            return DataUpload.objects.create(**kwargs)
        return make_data_upload


    def test_get_succeeds(self, url, admin_client, create_data_upload):
        create_data_upload(name='File 1')
        create_data_upload(name='File 2')

        response = admin_client.get(url)

        assert response.status_code == 200
        assert len(response.context_data['object_list']) == 2
