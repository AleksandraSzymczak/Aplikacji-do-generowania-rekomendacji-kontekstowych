from django.urls import path
from .views import data_docs, user_example

urlpatterns = [
    path('data_docs/', data_docs, name='Data_docs'),
    path('user_example/', user_example, name='User_example')
]