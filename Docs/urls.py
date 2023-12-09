from django.urls import path
from .views import data_docs, user_example, prefiltering, DCR, DCW


urlpatterns = [
    path('data_docs/', data_docs, name='Data_docs'),
    path('user_example/', user_example, name='User_example'),
    path('Prefiltering_doc/', prefiltering, name='Prefiltering_doc'),
    path('DCR_doc/', DCR, name='DCR_doc'),
    path('DCW_doc/', DCW, name='DCW_doc')
]