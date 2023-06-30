from django.urls import reverse

from core.tests.conftest import TemplateViewTestBase


class TestDataListListView(TemplateViewTestBase):
    url_name = 'main:datalist-list'

    def test_get_succeeds(self, url, create_subscribed_user, create_data_list):
        client, user1 = create_subscribed_user()
        _, user2 = create_subscribed_user()

        data_list1 = create_data_list(user=user1)
        data_list2 = create_data_list(user=user2)

        # Test authenticated user accessing own data lists
        client.force_login(user1)
        response = client.get(url)

        assert response.status_code == 200
        assert len(response.context['data_lists']) == 1
        assert data_list1 in response.context['data_lists']
        assert data_list2 not in response.context['data_lists']


    def test_get_unauthenticated_fails(self, url, client, settings):
        # Test unauthenticated user
        response = client.get(url)
        assert response.status_code == 302
        assert response.url.startswith(reverse(settings.LOGIN_URL))
