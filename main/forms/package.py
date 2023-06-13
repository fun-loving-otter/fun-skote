from django import forms

from main.models import DataPackageBenefits


class PackageChoiceForm(forms.Form):
    package_benefits = forms.ModelChoiceField(queryset=DataPackageBenefits.objects.all())
