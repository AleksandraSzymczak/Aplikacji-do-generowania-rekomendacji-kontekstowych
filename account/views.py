from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from rest_framework_simplejwt.views import TokenRefreshView
from DataPage.views import Files

def register(request):
    return render(request, 'account/login.html', )

@api_view(['POST'])
def register2(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Generate JWT token
            tokens = MyTokenObtainPairSerializer.get_token(user)
            tokens['access'] = str(tokens.access_token)

            return Response(tokens, status=200)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'token',
        'token/refresh',
    ]
    return Response(routes)


