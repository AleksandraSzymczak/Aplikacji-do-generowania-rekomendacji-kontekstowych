from django.urls import path
from .views import getRoutes, MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path, include
from .views import login_view


urlpatterns=[
    #path('', getRoutes),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', login_view, name='login')
]