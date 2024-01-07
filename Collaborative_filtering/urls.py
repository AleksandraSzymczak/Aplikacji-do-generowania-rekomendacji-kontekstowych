from django.urls import path, include
from .views import collaborative_filtering_page, Wyniki_collaborative_filtering, simulate_long_running_process, log_stream

urlpatterns = [
    path('collaborative_filtering_page/', collaborative_filtering_page, name='collaborative_filtering_page'),
    path('Wyniki_collaborative_filtering/', Wyniki_collaborative_filtering, name='Wyniki_collaborative_filtering'),
    path('collaborative_filtering_page/Wyniki_collaborative_filtering/simulate_long_running_process/<str:selected_file>/', simulate_long_running_process, name='simulate_long_running_process'),
    path('collaborative_filtering_page/Wyniki_collaborative_filtering/log-stream/', log_stream, name="log_stream")
]
