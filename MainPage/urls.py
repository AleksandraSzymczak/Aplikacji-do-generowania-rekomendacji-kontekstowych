from django.urls import path, include
from .views import home, upload_file, recommend
from account.views import register

urlpatterns = [
    path('', register, name='register'),
    path('mainpage/', home, name='home'),
    path('mainpage/prefiltering/', include('Prefiltering.urls')),
    path('mainpage/DCR/', include('DCR.urls')),
    path('mainpage/DCW/', include('DCW.urls')),
    #path('upload/', upload_file, name='upload_file'),
    path('mainpage/wybor_algorytmu/', recommend, name='wybor_algorytmu'),
]