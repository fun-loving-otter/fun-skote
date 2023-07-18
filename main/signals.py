from emails.models import EmailTemplate


def subscription_made_callback(sender, instance, **kwargs):
    subscription = instance.subscription

    # If this is not the first payment...
    if subscription.subscriptionpayment_set.count() > 1:
        return

    EmailTemplate.send("Subscription Created", subscription.user.email)
