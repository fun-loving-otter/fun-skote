import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_data_list_list_view_get(create_subscribed_user, create_data_list):
    client, user1 = create_subscribed_user()
    _, user2 = create_subscribed_user()

    data_list1 = create_data_list(user=user1)
    data_list2 = create_data_list(user=user2)

    # Test authenticated user accessing own data lists
    url = reverse('main:datalist-list')

    client.force_login(user1)
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.context['data_lists']) == 1
    assert data_list1 in response.context['data_lists']
    assert data_list2 not in response.context['data_lists']


    # Test authenticated user accessing other user's data lists
    client.force_login(user2)
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.context['data_lists']) == 1
    assert data_list1 not in response.context['data_lists']
    assert data_list2 in response.context['data_lists']



@pytest.mark.django_db
def test_data_list_list_view_unathenticated(client):
    url = reverse('main:datalist-list')

    # Test unauthenticated user
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('authentication:login')
