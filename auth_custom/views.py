from django.views.generic import TemplateView, FormView
from django.shortcuts import redirect
from django.contrib.auth import get_user_model

from authentication.views import RegisterView
from payments import models as payment_models
from auth_custom.forms import PaidRegistrationForm, InactiveUserForm

User = get_user_model()




def create_subscription(user, package):
    # Delete existing subscriptions:
    user.subscription_set.filter(status='n').delete()

    payment_models.Subscription.objects.create(
        user=user,
        recurring_price=package.price,
        products_info={
            'package': package.name,
            'credits': package.credits
        }
    )



class PaidRegisterView(RegisterView):
    form_class = PaidRegistrationForm
    success_url = 'authentication:payment-package'

    def form_valid(self, form):
        # Save user
        user = form.instance
        user.is_active = False
        form.save()
        user.update_country(self.request)

        # Store user in session since user can't be logged in.
        self.request.session['inactive_user_email'] = user.email

        create_subscription(user, form.cleaned_data['package'])

        return self.success()



class InactiveLoginCheckView(FormView):
    form_class = InactiveUserForm
    template_name = 'authentication/pages/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')

        return super().dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        email = form.cleaned_data.get('email')  # Assuming email is a field in your login form

        self.request.session['inactive_user_email'] = email  # Save user email in the session

        create_subscription(form.user, form.cleaned_data['package'])  # Create subscription for the user

        return redirect('authentication:payment-package')  # Redirect to the desired URL



class SubscriptionInitializeView(TemplateView):
    template_name = 'payments/subscriptions/initialize.html'

    def dispatch(self, request, *args, **kwargs):
        email = request.session.get('inactive_user_email')

        # Check if there exists a user with this email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return redirect('authentication:login-inactive')

        # If this user already has a subscription, redirect to proper login
        if user.is_active:
            return redirect('authentication:login')

        self.inactive_user = user

        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self):
        context = super().get_context_data()
        user = self.inactive_user

        # Attach settings and general info to context
        context['settings'] = payment_models.PaymentSettings.load()
        context['currencies'] = payment_models.Currency.objects.filter(visible=True)

        # Attach new subscription to context
        query = user.subscription_set.filter(status='n')
        if query.exists():
            context['subscription'] = query.first()

            # test
            sub = context['subscription']
            print(sub.product)

        return context
