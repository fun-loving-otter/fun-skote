import os
from django import forms

from main.models import DataUpload, UploadedDataFile
from main.tasks.task_parse_uploaded_file import parse_uploaded_file
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError


class MultipleFileNameField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', forms.HiddenInput())
        super().__init__(*args, **kwargs)


    def to_python(self, value):
        """Convert strings into list of strings"""
        if not value:
            return []

        if isinstance(value, str):
            return value.split(',')

        return list(value)




class DataUploadForm(forms.ModelForm):
    files = MultipleFileNameField()

    class Meta:
        model = DataUpload
        fields = ['name']


    def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)


    def clean_files(self):
        """Check if all provided files exist"""
        filenames = self.cleaned_data['files']
        upload_temp_dir = UploadedDataFile.get_upload_temp_dir(self.user)

        filepaths = []
        for filename in filenames:
            filepath = upload_temp_dir / filename
            if not os.path.isfile(filepath):
                raise ValidationError(f"No file found at {filepath}")
            filepaths.append(filepath)

        print(filepaths)
        return filepaths


    def save(self, commit=True):
        '''
        Reads files from tmp location, reads them into memory and creates UploadedDataFile
        Starts processing tasks
        '''
        filepaths = self.cleaned_data.get('files', [])
        files = []
        for path in filepaths:
            with open(path, 'rb') as f:
                content = f.read()
                name = os.path.basename(path)
                file = ContentFile(content, name=name)
                files.append(file)
            os.remove(path)

        self.instance.size_of_files = sum(f.size for f in files)
        self.instance.number_of_files = len(files)

        data_upload = super().save(commit=commit)

        for file in files:
            # Create UploadedDataFile
            uploaded_data_file = UploadedDataFile.objects.create(
                data_upload=data_upload,
                file=file,
            )

            # Start processing task (requires id created on save)
            result = parse_uploaded_file.delay(uploaded_data_file.id)

            # Assign task_id to UploadedDataFile
            UploadedDataFile.objects.filter(id=uploaded_data_file.id).update(celery_task_id=result.task_id)

        return data_upload




class DropzoneFileUploadForm(forms.Form):
    file = forms.FileField()
    dzuuid = forms.CharField()
    dztotalchunkcount = forms.IntegerField()
    dzchunkindex = forms.IntegerField()

    def __init__(self, *args, user, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)


    def save(self):
        '''
        Accepts a file in chunks and saves each chunk in a separate file in tmp location
        After last chunk is uploaded, merges them all into one file
        '''
        file = self.cleaned_data['file']
        upload_id = self.cleaned_data['dzuuid']
        chunk_index = self.cleaned_data['dzchunkindex']
        total_chunks = self.cleaned_data['dztotalchunkcount']

        # Where to save chunks
        upload_temp_dir = UploadedDataFile.get_upload_temp_dir(self.user)

        # Save chunk
        chunk_name = UploadedDataFile.get_chunk_name(file, upload_id, chunk_index)
        chunk_path = upload_temp_dir / chunk_name
        with open(chunk_path, 'wb') as chunk_file:
            for chunk in file.chunks():
                chunk_file.write(chunk)

        # If it is the last chunk, save the file
        if chunk_index + 1 == total_chunks:
            chunks = []
            for i in range(total_chunks):
                chunk_name = UploadedDataFile.get_chunk_name(file, upload_id, i)
                chunk_path = upload_temp_dir / chunk_name
                with open(chunk_path, 'rb') as chunk_file:
                    chunks.append(chunk_file.read())

                # Cleanup
                os.remove(chunk_path)

            # Save concatenated file
            file_content = b''.join(chunks)
            filename = UploadedDataFile.get_file_name(file, upload_id)
            with open(upload_temp_dir / filename, 'wb') as f:
                f.write(file_content)

        # bool is_last_chunk
        return chunk_index + 1 == total_chunks
