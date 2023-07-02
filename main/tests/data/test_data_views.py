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


    def test_date_filters(self, url, create_subscribed_user, create_data_upload, create_data):
        client, user = create_subscribed_user(api=True)

        data_upload, uploaded_data_file = create_data_upload()

        data1 = create_data(uploaded_data_file)
        data2 = create_data(uploaded_data_file, founded_date="2023-01-01", last_funding_date="2022-06-01")

        data = {'filters': {
            'founded_date_after': '2022-01-01',
            'last_funding_date_before': '2022-12-31'
        }}
        response = client.post(url, data, format='json')

        # Assert the response status code and the filtered queryset
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['id'] == data2.id


    # def test_integer_filters(self, url, create_subscribed_user, create_data_upload, create_data):
    #     client, user = create_subscribed_user(api=True)

    #     data_upload, uploaded_data_file = create_data_upload()

    #     data1 = create_data(uploaded_data_file, number_of_employees=100, total_funding_amount=1000000)
    #     data2 = create_data(uploaded_data_file, number_of_employees=500, total_funding_amount=5000000)

    #     data = {'filters': {
    #         'number_of_employees_min': 200,
    #         'total_funding_amount_max': 3000000
    #     }}
    #     response = client.post(url, data, format='json')

    #     # Assert the response status code and the filtered queryset
    #     assert response.status_code == status.HTTP_200_OK
    #     assert len(response.data['results']) == 1
    #     assert response.data['results'][0]['id'] == data1.id
