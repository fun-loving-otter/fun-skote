from django import forms
from django.core.exceptions import ValidationError


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



class PeriodForm(forms.Form):
	start = forms.DateTimeField()
	end = forms.DateTimeField()
