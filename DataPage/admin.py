from django import forms
from django.contrib import admin
from django.utils.html import format_html
from .models import Files

class FilesAdminForm(forms.ModelForm):
    class Meta:
        model = Files
        fields = '__all__'

    file_content = forms.FileField()

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.file_content = self.cleaned_data['file_content'].read()
        if commit:
            instance.save()
        return instance

class FilesAdmin(admin.ModelAdmin):
    form = FilesAdminForm
    list_display = ['user', 'file_name', 'description', 'uploaded_at']
    search_fields = ['user__username', 'file_name', 'description']

    def display_file(self, obj):
        return format_html('<a href="{}" download>{}</a>', obj.file_name, obj.file_name)

    display_file.short_description = 'File'
    display_file.allow_tags = True

admin.site.register(Files, FilesAdmin)
