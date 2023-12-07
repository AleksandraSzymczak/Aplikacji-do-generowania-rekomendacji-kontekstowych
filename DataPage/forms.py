from django import forms
from .models import Files

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = Files
        fields = ['file_name', 'file_content', 'description']

    file_content = forms.FileField()

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.file_content = self.cleaned_data['file_content'].read()
        if commit:
            instance.save()
        return instance
