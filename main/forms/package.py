from django import forms

from main.models import Package


class PackageChoiceForm(forms.Form):
    package = forms.ModelChoiceField(queryset=Package.objects.all())
