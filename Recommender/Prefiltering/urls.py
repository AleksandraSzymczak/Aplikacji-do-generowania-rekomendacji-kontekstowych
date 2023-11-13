from django.urls import path
from .views import prefiltering_page, Wyniki_prefiltering, simulate_long_running_process

urlpatterns = [
    path('prefiltering_page/', prefiltering_page, name='prefiltering_page'),
    path('Wyniki_prefiltering/', Wyniki_prefiltering, name='Wyniki_prefiltering'),
    path('simulate_long_running_process/', simulate_long_running_process, name='simulate_long_running_process'),

]