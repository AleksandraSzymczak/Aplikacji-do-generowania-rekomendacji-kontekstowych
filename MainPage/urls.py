from django.urls import path
from .views import home, upload_file, recommend
from account.views import register

urlpatterns = [
    path('', register, name='register'),
    path('mainpage/', home, name='home'),
    #path('upload/', upload_file, name='upload_file'),
    path('wybor_algorytmu/', recommend, name='wybor_algorytmu'),
]