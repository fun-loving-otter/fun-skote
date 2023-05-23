from django import forms
from main.models import DataUpload, UploadedDataFile



class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True



class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result



class DataUploadForm(forms.ModelForm):
    csv_files = MultipleFileField()

    class Meta:
        model = DataUpload
        fields = ['name']

    def save(self, commit=True):
        data_upload = super().save(commit=commit)
        csv_files = self.cleaned_data.get('csv_files')
        if csv_files:
            for csv_file in csv_files:
                uploaded_data_file = UploadedDataFile(data_upload=data_upload, file=csv_file)
                uploaded_data_file.save()
        return data_upload
