from django.db import models
from account.models import CustomUser

class Files(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to='user_files/')
    FILE_CHOICES = (
    ("LOG", "log"),
    ("BINARY", "binary"),
    ("COMPACT", "March"),
    ("LOOSE", "loose"),)

    description = models.CharField(max_length=9,
                    choices=FILE_CHOICES,
                    default="LOG")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} - {self.file.name}"
