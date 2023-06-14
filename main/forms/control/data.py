from django import forms
from main.models import DataUpload, UploadedDataFile
from main import tasks


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
        csv_files = self.cleaned_data.get('csv_files', [])
        self.instance.size_of_files = sum(x.size for x in csv_files)
        self.instance.number_of_files = len(csv_files)

        data_upload = super().save(commit=commit)

        if csv_files:
            for csv_file in csv_files:
                uploaded_data_file = UploadedDataFile(
                    data_upload=data_upload,
                    file=csv_file,
                )
                uploaded_data_file.save()
                tasks.parse_csv_file.delay(uploaded_data_file.id)

        return data_upload
