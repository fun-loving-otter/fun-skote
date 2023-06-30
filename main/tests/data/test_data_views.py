from rest_framework import status

from core.tests.conftest import TemplateViewTestBase, ViewTestBase


class TestDataListView(TemplateViewTestBase):
    url_name = 'main:data-list'

    def test_get_succeeds(self, url, create_subscribed_user, create_data_list):
        client, user = create_subscribed_user()
        data_list = create_data_list(user)

        response = client.get(url)

        assert response.status_code == 200
        assert data_list in response.context['datalists']



class TestDataAPIListView(ViewTestBase):
    url_name = 'main:api-data-list'

    def test_post_succeeds(self, url, create_subscribed_user, created_data):
        client, user = create_subscribed_user()

        response = client.post(url)

        assert response.status_code == status.HTTP_200_OK

        data = response.data
        assert data['count'] == created_data.uploadeddatafile_set.first().data_set.count()
