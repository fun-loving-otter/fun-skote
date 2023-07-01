import pytest

from django.urls import reverse

from rest_framework import status

from core.tests.conftest import ViewTestBase
from main.models import DataList



class TestDataListAPIDestroyView(ViewTestBase):
    url_name = 'main:api-datalist-delete'

    @pytest.fixture(autouse=True)
    def always_create_data(self, created_data):
        self.created_data = created_data
        return self.created_data


    @pytest.fixture
    def data_list(self, create_subscribed_user, create_data_list):
        self.client, self.user = create_subscribed_user(api=True)
        self.created_data_list = create_data_list(self.user)
        return self.created_data_list


    @pytest.fixture
    def url(self, data_list):
        return reverse(self.url_name, kwargs={'pk': data_list.pk})


    def test_delete_destroy_succeeds(self, url):
        client = self.client
        data_list = self.created_data_list

        response = client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert DataList.objects.filter(pk=data_list.pk).exists() is False


    def test_delete_other_user_fails(self, url, create_subscribed_user, create_data_list):
        client, other_user = create_subscribed_user(api=True)
        data_list = create_data_list(user=other_user)

        response = client.delete(url)

        assert response.status_code == 404

        assert DataList.objects.filter(pk=data_list.pk).exists() is True
