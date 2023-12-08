from django.db import models
from django.conf import settings
from account.models import CustomUser


class Files(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file_content = models.BinaryField(editable=True)
    FILE_CHOICES = (
        ("LOG", "log"),
        ("BINARY", "binary"),
        ("COMPACT", "compact"),
        ("LOOSE", "loose"),
    )

    description = models.CharField(
        max_length=9,
        choices=FILE_CHOICES,
        default="LOG",
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.file_name}"

    def save_uploaded_file(self, uploaded_file):
        self.file_name = uploaded_file.name
        with uploaded_file.open(mode='rb') as file:
            self.file_content = file.read()

        self.save()