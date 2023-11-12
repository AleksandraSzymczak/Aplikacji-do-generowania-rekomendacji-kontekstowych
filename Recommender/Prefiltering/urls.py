from django.urls import path
from .views import prefiltering_page

urlpatterns = [
    path('prefiltering_page/', prefiltering_page, name='prefiltering_page'),
]