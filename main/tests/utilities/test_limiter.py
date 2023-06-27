import pytest

from django.test import RequestFactory

from main.models import UserThrottledActionEntry
from main.utilities import Limiter


@pytest.fixture
def limiter():
    return Limiter()


@pytest.fixture
def request_factory():
    return RequestFactory()


@pytest.fixture
def user_request(request_factory):
    def make_request(user):
        request = request_factory.get('/')
        request.user = user
        request.subscription = getattr(user, 'subscription', None)
        return request
    return make_request



@pytest.mark.django_db
def test_limiter_allow_request_authenticated(limiter, create_subscribed_user, user_request):
    client, user = create_subscribed_user()

    request = user_request(user)

    assert limiter.allow_request(request, 'Action Name', 1)



@pytest.mark.django_db
def test_limiter_allow_request_unauthenticated(limiter, create_user, user_request):
    user = create_user()

    request = user_request(user)

    assert not limiter.allow_request(request, 'Action Name', 1)



@pytest.mark.django_db
def test_limiter_allow_request_superuser(limiter, create_user, user_request):
    user = create_user(is_superuser=True)

    request = user_request(user)

    assert limiter.allow_request(request, 'Action Name', 1)



@pytest.mark.django_db
def test_limiter_allow_request_staff(limiter, create_user, user_request):
    user = create_user(is_staff=True)

    request = user_request(user)

    assert limiter.allow_request(request, 'Action Name', 1)



@pytest.mark.django_db
def test_limiter_allow_request_exceed_limit(limiter, create_subscribed_user, user_request):
    client, user = create_subscribed_user()
    request = user_request(user)
    action_name = 'Action Name'
    action_cost = limiter.get_user_rate(request)  # Should be equal to users' credits amount

    # Create action entries that exceed the rate limit
    for _ in range(10):
        UserThrottledActionEntry.objects.create(user=user, action=action_name, amount=action_cost)

    assert not limiter.allow_request(request, action_name, action_cost)
