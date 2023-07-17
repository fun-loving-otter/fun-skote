from main.models import DataList
from core.tests.conftest import TemplateViewTestBase


class TestDataListCreateView(TemplateViewTestBase):
    url_name = 'main:datalist-create'

    def test_get_succeeds(self, url, create_subscribed_user):
        client, user = create_subscribed_user()
        response = client.get(url)
        assert response.status_code == 200
        assert 'form' in response.context


    def test_post_creation_succeeds(self, url, create_subscribed_user):
        client, user = create_subscribed_user()

        # Create the form data for the new data list
        form_data = {
            'name': 'Test Data List',
        }

        # Make a POST request to the data list create view using the client
        response = client.post(url, data=form_data)

        # Assert the response status code is 302 (redirect)
        assert response.status_code == 302

        # Get the created data list from the database
        data_list = DataList.objects.filter(name=form_data['name']).first()

        assert data_list is not None
        assert data_list.creator == user
