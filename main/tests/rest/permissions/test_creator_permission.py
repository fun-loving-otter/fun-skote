import pytest

from django.contrib.auth.models import AnonymousUser

from rest_framework.test import APIRequestFactory

from main.rest.permissions import IsCreatorPermission


@pytest.mark.django_db
@pytest.mark.skip(reason="Permission removed")
class TestIsCreatorPermission:
    @pytest.fixture
    def data_list(self, create_user, create_data_list):
        user = create_user()
        data_list = create_data_list(user)
        return data_list


    @pytest.fixture
    def request_base(self):
        factory = APIRequestFactory()
        request = factory.get('test')
        return request


    @pytest.fixture
    def creator_request(self, request_base, data_list):
        request_base.user = data_list.creator
        return request_base


    @pytest.fixture
    def different_user_request(self, request_base, create_user):
        request_base.user = create_user()
        return request_base


    @pytest.fixture
    def anonymous_request(self, request_base):
        request_base.user = AnonymousUser()
        return request_base


    @pytest.mark.parametrize('request_fixture, expected_result', [
        ['creator_request', True],
        ['different_user_request', False],
        ['anonymous_request', False],
    ])
    def test_request_result(self, request_fixture, expected_result, data_list, request):
        r = request.getfixturevalue(request_fixture)
        permission = IsCreatorPermission()
        has_permission = permission.has_object_permission(r, None, data_list)
        assert has_permission is expected_result
