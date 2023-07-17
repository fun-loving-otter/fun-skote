from django import forms

from main.models import DataList


class DataListForm(forms.ModelForm):
    class Meta:
        model = DataList
        fields = ['name']
