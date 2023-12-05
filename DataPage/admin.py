from django import forms
from django.contrib import admin
from .models import Files

class FilesAdminForm(forms.ModelForm):
    class Meta:
        model = Files
        fields = '__all__'

    def clean_file(self):
        file = self.cleaned_data['file']
        return file

class FilesAdmin(admin.ModelAdmin):
    form = FilesAdminForm
    list_display = ['user', 'file', 'description', 'uploaded_at']
    search_fields = ['user__username', 'file', 'description']

admin.site.register(Files, FilesAdmin)
