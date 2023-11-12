from django.urls import path
from .views import DCR_page

urlpatterns = [
    path('DCR_page/', DCR_page, name='DCR_page'),
]