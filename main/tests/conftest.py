import pytest

from authentication.tests.conftest import *
from payments.tests.conftest import *
from main.models import DataList, DataPackageBenefits


@pytest.fixture
def create_subscribed_user(auto_login_user, create_active_subscription):
    def make():
        client, user = auto_login_user()
        subscription = create_active_subscription(user)
        DataPackageBenefits.objects.create(
            credits=5000,
            package=subscription.package
        )
        # Half-ass the attachment
        user.subscription = subscription
        return client, user
    return make



@pytest.fixture
def create_data_list():
    def make_data_list(user):
        return DataList.objects.create(
            creator=user,
            name='Test Data List',
            source='Test Source'
        )
    return make_data_list
