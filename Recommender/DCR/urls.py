from django.urls import path
from .views import DCR_page, Wyniki

urlpatterns = [
    path('DCR_page/', DCR_page, name='DCR_page'),
    path('wyniki/', Wyniki, name='Wyniki'),
]