import pytest

from payments.consts import subscription_status


@pytest.mark.django_db
def test_subscription_creation_sends_email_to_customer(create_user, create_subscription, create_subscription_package, create_subscription_payment, mailoutbox):
    customer = create_user()

    # Create a subscription with the referrer information
    package = create_subscription_package(price=10)
    subscription = create_subscription(
        customer,
        status=subscription_status.WAITING_FOR_VALIDATION,
        package=package
    )

    # Add payment to subscription
    # This will trigger subscription_paid signal
    create_subscription_payment(subscription, -30, 10)

    assert len(mailoutbox) > 0

    for mail in mailoutbox:
        if customer.email in mail.to:
            break
    assert customer.email in mail.to
