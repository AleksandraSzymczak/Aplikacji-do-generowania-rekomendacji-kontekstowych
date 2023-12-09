from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from rest_framework_simplejwt.views import TokenRefreshView
from DataPage.views import Files
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from .models import CustomUser


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/mainpage/')
    else:
        form = AuthenticationForm()

    return render(request, 'account/login.html', {'form': form})


def signup_view(request):
    return render(request, 'account/register.html')


def registration_view(request):
    if request.method == 'POST':
        print(request.POST)
        email_to_check = request.POST.get('email')
        password = request.POST.get('password1')
        username_to_check = request.POST.get('username')
        if CustomUser.objects.filter(email=email_to_check).exists():
            messages.error(request, 'This email is already registered. Please use a different email.')
            return redirect('registration') 
        
        if CustomUser.objects.filter(username=username_to_check).exists():
            messages.error(request, 'This Username is already registered. Please use a different username.')
            return redirect('registration') 

        new_user = CustomUser.objects.create_user(username=username_to_check, email=email_to_check, password=password)
        user = authenticate(request, username=username_to_check, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'There was an error logging in. Please try again.')
    return render(request, 'account/register.html')


def logout_view(request):
    logout(request)
    return redirect('/')


def register(request):
    return render(request, 'account/login.html', )


@api_view(['POST'])
def register2(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

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
