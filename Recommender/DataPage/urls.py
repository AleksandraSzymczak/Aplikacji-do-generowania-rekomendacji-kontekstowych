from django.urls import path
from .views import FileUploadView, FileDeleteView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='upload_file'),
    path('delete/<int:file_id>/', FileDeleteView.as_view(), name='delete_file'),
]