import pytest

from django.test import RequestFactory

from main.utilities import Limiter
from main.consts import action_names
from main.models import UserThrottledActionEntry
from main.mixins import DataPackageCheckerMixin


def get_subscription_from_request(request):
    user = request.user
    subscription_checker = DataPackageCheckerMixin()
    return subscription_checker.get_subscription(user=user)


@pytest.mark.django_db
class TestLimiter:
    @pytest.fixture(autouse=True)
    def limiter(self):
        self.limiter = Limiter()
        self.limiter.get_user_subscription = get_subscription_from_request
        return self.limiter


    @pytest.fixture(autouse=True)
    def request_factory(self):
        self.request_factory = RequestFactory()
        return self.request_factory


    @pytest.fixture
    def user_request(self, request_factory):
        def make_request(user):
            request = self.request_factory.get('/')
            request.user = user
            return request
        return make_request


    def test_subscribed_user_returns_true(self, create_subscribed_user, user_request):
        client, user = create_subscribed_user()
        request = user_request(user)
        assert self.limiter.allow_request(request, action_names.ACTION, 1) is True


    def test_anonymous_user_returns_false(self, create_user, user_request):
        user = create_user()
        request = user_request(user)
        assert self.limiter.allow_request(request, action_names.ACTION, 1) is False


    def test_superuser_returns_true(self, admin_user, user_request):
        request = user_request(admin_user)
        assert self.limiter.allow_request(request, action_names.ACTION, 1) is True


    def test_staff_returns_true(self, create_user, user_request):
        user = create_user(is_staff=True)
        request = user_request(user)
        assert self.limiter.allow_request(request, action_names.ACTION, 1) is True


    def test_limit_exceeded_returns_false(self, create_subscribed_user, user_request):
        client, user = create_subscribed_user()
        request = user_request(user)
        action_name = action_names.ACTION
        action_cost = self.limiter.get_user_rate(request, action_name)  # Should be equal to users' credits amount

        # Create action entries that exceed the rate limit
        for _ in range(10):
            UserThrottledActionEntry.objects.create(user=user, action=action_name, amount=action_cost)

        assert self.limiter.allow_request(request, action_name, action_cost) is False
