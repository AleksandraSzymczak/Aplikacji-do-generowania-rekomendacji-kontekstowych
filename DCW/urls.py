from django.urls import path
from .views import DCW_page, Wyniki_DCW
from Collaborative_filtering.views import simulate_long_running_process

urlpatterns = [
    path('DCW_page/', DCW_page, name='DCW_page'),
    path('Wyniki_DCW/', Wyniki_DCW, name='Wyniki_DCW'),
    path('Wyniki_prefiltering/simulate_long_running_process/', simulate_long_running_process, name='simulate_long_running_process'),
]