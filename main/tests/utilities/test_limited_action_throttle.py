import pytest

from django.urls import reverse

from main.models import DataPackageBenefits


@pytest.fixture
def rate_limit():
    return 10



@pytest.mark.django_db
@pytest.mark.urls('main.tests.urls_pytest')
def test_limited_action_throttle_user(auto_login_user, rate_limit, create_active_subscription):
    client, user = auto_login_user(api=True)

    subscription = create_active_subscription(user)
    DataPackageBenefits.objects.create(
        action_credits=rate_limit,
        export_credits=rate_limit,
        add_to_list_credits=rate_limit,
        package=subscription.package
    )

    # Make requests within the rate limit
    for _ in range(rate_limit):
        response = client.get(reverse('limited-action-view'))
        assert response.status_code == 200

    # Make one more request that exceeds the rate limit
    response = client.get(reverse('limited-action-view'))
    assert response.status_code == 429

    # Test throttle interference
    # Request limit on another view shouldn't be affected
    response = client.get(reverse('limited-action-view2'))
    assert response.status_code == 200
