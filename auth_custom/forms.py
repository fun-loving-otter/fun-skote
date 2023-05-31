from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div

from authentication.forms import UserRegistrationForm
from main.models import Package


User = get_user_model()



class PaidRegistrationForm(UserRegistrationForm):
    package = forms.ModelChoiceField(queryset=Package.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Div('email', css_class='mb-3'),
            Div('first_name', css_class='mb-3'),
            Div('last_name', css_class='mb-3'),
            Div('password1', css_class='mb-3'),
            Div('password2', css_class='mb-3'),
            Div('package', css_class='mb-3'),
            Div(
                Submit('submit', _('Register'), css_class="btn btn-primary waves-effect waves-light"),
                css_class="d-grid"
            )
        )



class InactiveUserForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    package = forms.ModelChoiceField(queryset=Package.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div('email', css_class='mb-3'),
            Div('password', css_class='mb-3'),
            Div('package', css_class='mb-3'),
            Div(
                Submit('submit', _('Login'), css_class="btn btn-primary waves-effect waves-light"),
                css_class="d-grid"
            )
        )


    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError('Invalid email or password.')

        if user.is_active:
            raise forms.ValidationError('Invalid email or password.')

        if not user.check_password(password):
            raise forms.ValidationError('Invalid email or password.')

        self.user = user

        return cleaned_data
