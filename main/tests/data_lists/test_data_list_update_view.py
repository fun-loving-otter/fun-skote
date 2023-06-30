import pytest

from django.urls import reverse

from core.tests.conftest import ViewTestBase

class TestDataListAPIListView(ViewTestBase):
    url_name = 'main:api-datalist-update'

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


    def test_patch_update_succeeds(self, url):
        client = self.client
        data_list = self.created_data_list

        # First request
        patch_data = {
            'data': [1, 5, 8]
        }
        response = client.patch(url, patch_data, format='json')
        data_list.refresh_from_db()

        assert response.status_code == 200
        assert set(data_list.data.values_list('pk', flat=True)) == set(patch_data['data'])


        # Second request
        patch_data2 = {
            'data': [2]
        }
        response = client.patch(url, patch_data2, format='json')
        data_list.refresh_from_db()

        assert response.status_code == 200
        assert set(data_list.data.values_list('pk', flat=True)) == set(patch_data['data'] + patch_data2['data'])


    def test_patch_other_user_fails(self, url, create_subscribed_user, create_data_list):
        client = self.client

        _, other_user = create_subscribed_user(api=True)
        data_list = create_data_list(user=other_user)

        # Attempt to update the DataList object belonging to the other user
        patch_data = {
            'data': [1, 5, 8]
        }
        response = client.patch(url, patch_data, format='json')
        data_list.refresh_from_db()

        assert response.status_code == 404
        assert set(data_list.data.values_list('pk', flat=True)) != set(patch_data['data'])


    def test_patch_anonymous_user_fails(self, url, api_client):
        api_client.logout()

        patch_data = {
            'data': [1, 5, 8]
        }

        response = api_client.patch(url, patch_data, format='json')
        assert response.status_code == 403
