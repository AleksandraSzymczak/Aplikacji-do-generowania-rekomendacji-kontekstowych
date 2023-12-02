from django.urls import path
from .views import DCR_page, Wyniki, simulate_long_running_process

urlpatterns = [
    path('DCR_page/', DCR_page, name='DCR_page'),
    path('wyniki/', Wyniki, name='Wyniki'),
    path('wyniki/simulate_long_running_process/', simulate_long_running_process, name='simulate_long_running_process'),
]