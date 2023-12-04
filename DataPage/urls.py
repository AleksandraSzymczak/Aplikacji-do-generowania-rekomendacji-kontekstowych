from django.urls import path
from .views import FileUploadView, FileDeleteView, FileDownloadView, Data_page, transform

urlpatterns = [
    path('', Data_page, name='Data_page'),
    path('upload/', FileUploadView.as_view(), name='upload_file'),
    path('delete/', FileDeleteView.as_view(), name='delete_files'),
    path('download/<str:file_id>/', FileDownloadView.as_view(), name='download'),
    path('handle_option_click/', transform, name="transform")
]