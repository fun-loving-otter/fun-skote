from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from django.urls import reverse

from main.forms.package import PackageChoiceForm
from payments.models import Subscription
from payments.consts import subscription_status
from payments.utilities import SubscriptionChecker



class PackageChoiceView(SubscriptionChecker, LoginRequiredMixin, FormView):
    template_name = 'main/package/package_choice.html'
    form_class = PackageChoiceForm
    subscription_queryset = Subscription.objects.exclude(package__datapackagebenefits=None)

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if self.get_subscription(user, status=subscription_status.ACTIVE):
            return redirect(reverse('index'))

        if self.get_subscription(user, status=subscription_status.NEW):
            return redirect(reverse('payments:subscription'))

        return super().dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        benefits = form.cleaned_data['package_benefits']
        package = benefits.package

        # Create Subscription
        Subscription.objects.create(
            user=self.request.user,
            recurring_price=package.price,
            products_info=[
                {
                    'Package Name': package.name,
                    'Credits': benefits.credits
                }
            ],
            package=package,
            extra_info={
                'referrer': self.request.session.get('referrer')
            }
        )

        return redirect(reverse('payments:subscription'))
