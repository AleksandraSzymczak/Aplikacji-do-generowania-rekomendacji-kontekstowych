from django.urls import path
from .views import DCW_page, Wyniki_DCW

urlpatterns = [
    path('DCW_page/', DCW_page, name='DCW_page'),
    path('Wyniki_DCW/', Wyniki_DCW, name='Wyniki_DCW')
]