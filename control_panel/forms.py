from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div

User = get_user_model()


def validate_file_extension(value):
	if not value.name.endswith('.xlsx'):
		raise ValidationError('Wrong file extension. Only .xlsx files allowed', params={"value": value})



def create_wysi_editor():
	widget = forms.Textarea(
		{"class": "wysi"}
	)
	return widget



class ImportExcelForm(forms.Form):
	table = forms.FileField(
		validators=[validate_file_extension],
		widget=forms.ClearableFileInput(
			attrs={
				'class': 'form-control'
			}
		)
	)



class UserCreationForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['password', 'email', 'first_name', 'last_name', 'is_active']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['email'].required = True
		self.fields['email'].validators

		self.helper = FormHelper()
		self.helper.layout = Layout(
			Div('email', css_class='mb-3'),
			Div('password', css_class='mb-3'),
			Row(
				Column('first_name', css_class='col-md-6 mb-0'),
				Column('last_name', css_class='col-md-6 mb-0'),
				css_class='row mb-3'
			),
			Div('is_active', css_class='mb-3 lh-1'),
			Submit('submit', 'Create')
		)

	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			raise ValidationError("Email already exists")
		return email

	def save(self, *args, **kwargs):
		self.instance.set_password(self.cleaned_data['password'])
		super().save(*args, **kwargs)



class AdminProfileForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['available_pages']
		widgets = {
			"available_pages": forms.CheckboxSelectMultiple()
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		submit_id = self.instance.pk if self.instance else None
		self.helper.layout = Layout(
			'available_pages',
			Submit('submit', 'Update', css_id=submit_id)
		)



class PeriodForm(forms.Form):
	start = forms.DateTimeField()
	end = forms.DateTimeField()
