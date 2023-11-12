from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    upload_date = models.DateTimeField(auto_now_add=True)
    def get_file_path(self):
        return self.file.path