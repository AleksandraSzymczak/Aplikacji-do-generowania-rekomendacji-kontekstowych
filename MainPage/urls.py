from django.urls import path, include
from .views import HomeView, upload_file, recommend
from account.views import register
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


urlpatterns = [
    path('', register, name='register'),
    #path('mainpage/', HomeView.as_view(), name='home'),
    path('mainpage/prefiltering/', include('Prefiltering.urls')),
    path('mainpage/DCR/', include('DCR.urls')),
    path('mainpage/DCW/', include('DCW.urls')),
    path('mainpage/', HomeView.as_view(), name='home'),
    #path('upload/', upload_file, name='upload_file'),
    path('mainpage/wybor_algorytmu/', recommend, name='wybor_algorytmu'),
]