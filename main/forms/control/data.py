from django import forms

from main.models import DataUpload, UploadedDataFile
from main.tasks.task_parse_uploaded_file import parse_uploaded_file


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
    files = MultipleFileField()

    class Meta:
        model = DataUpload
        fields = ['name']

    def save(self, commit=True):
        files = self.cleaned_data.get('files', [])
        self.instance.size_of_files = sum(x.size for x in files)
        self.instance.number_of_files = len(files)

        data_upload = super().save(commit=commit)

        if files:
            for file in files:
                # Create UploadedDataFile
                uploaded_data_file = UploadedDataFile(
                    data_upload=data_upload,
                    file=file,
                )
                uploaded_data_file.save()

                # Start processing task (requires id created on save)
                result = parse_uploaded_file.delay(uploaded_data_file.id)

                # Assign task_id to UploadedDataFile
                UploadedDataFile.objects.filter(id=uploaded_data_file.id).update(celery_task_id=result.task_id)

        return data_upload
