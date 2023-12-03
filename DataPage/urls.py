from django.urls import path
from .views import FileUploadView, FileDeleteView, FileDownloadView, Data_page

urlpatterns = [
    path('', Data_page, name='Data_page'),
    path('upload/', FileUploadView.as_view(), name='upload_file'),
    path('delete/', FileDeleteView.as_view(), name='delete_files'),
    path('download/<int:file_id>/', FileDownloadView.as_view(), name='download'),
]