import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_data_list_list_view_get(create_subscribed_user, create_data_list, created_data):
    client, user = create_subscribed_user(api=True)

    data_list = create_data_list(user=user)


    # First request
    patch_data = {
        'data': [1, 5, 8]
    }

    url = reverse('main:api-datalist-update', kwargs={'pk': data_list.pk})
    response = client.patch(url, patch_data, format='json')

    assert response.status_code == 200

    data_list.refresh_from_db()

    assert set(data_list.data.values_list('pk', flat=True)) == set(patch_data['data'])

    patch_data2 = {
        'data': [2]
    }


    # Second request
    response = client.patch(url, patch_data2, format='json')

    assert response.status_code == 200

    data_list.refresh_from_db()

    assert set(data_list.data.values_list('pk', flat=True)) == set(patch_data['data'] + patch_data2['data'])



@pytest.mark.django_db
def test_data_list_update_view_access(create_subscribed_user, create_data_list, create_user):
    client, user = create_subscribed_user(api=True)
    other_user = create_user()

    # Create a DataList object belonging to the other user
    data_list = create_data_list(user=other_user)

    # Attempt to update the DataList object belonging to the other user
    patch_data = {
        'data': [1, 5, 8]
    }
    url = reverse('main:api-datalist-update', kwargs={'pk': data_list.pk})
    response = client.patch(url, patch_data, format='json')

    # Assert that the response status code is 403 Forbidden
    assert response.status_code == 403

    # Assert that the DataList object has not been updated
    data_list.refresh_from_db()
    assert set(data_list.data.values_list('pk', flat=True)) != set(patch_data['data'])



@pytest.mark.django_db
def test_data_list_list_view_unathenticated(api_client, create_user, create_data_list):
    user = create_user()
    data_list = create_data_list(user=user)

    url = reverse('main:api-datalist-update', kwargs={'pk': data_list.pk})

    patch_data = {
        'data': [1, 5, 8]
    }

    response = api_client.patch(url, patch_data, format='json')
    # Since throttle also blocks unauthenticated requests, check for multiple codes
    # To check if either permission or throttle caugth the request
    assert response.status_code in [429, 403]
