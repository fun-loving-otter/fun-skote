from django.shortcuts import redirect
from django.views.generic import FormView
from django.urls import reverse

from payments.models import Subscription
from main.models import PackageSubscription
from main.forms.package import PackageChoiceForm


class PackageChoiceView(FormView):
    template_name = 'main/package/package_choice.html'
    form_class = PackageChoiceForm

    def form_valid(self, form):
        package = form.cleaned_data['package']

        # Create Subscription
        subscription = Subscription.objects.create(
            user=self.request.user,
            recurring_price=package.price,
            products_info=[
                {
                    'Package Name': package.name,
                    'Credits': package.credits
                }
            ]
        )

        # Create PackageSubscription
        PackageSubscription.objects.create(
            user=self.request.user,
            package=package,
            subscription=subscription
        )

        return redirect(reverse('subscription-init'))
