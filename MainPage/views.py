from django.shortcuts import render
from django.core.files.storage import default_storage
from .forms import FileUploadForm
from django.shortcuts import render, redirect
from DataPage.views import Files
from django.views import View
from django.http import JsonResponse
from django.urls import reverse
import json
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(View, LoginRequiredMixin):
    def get(self, request):
        current_user = request.user
        print(current_user)
        files = Files.objects.filter(user=current_user).order_by('-uploaded_at')
        file_des_dict = {file.file_name: file.description for file in files}
        print(file_des_dict)
        return render(request, 'MainPage/main.html', {'pliki_dict': file_des_dict})


def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            success_message = "Plik został pomyślnie przesłany."

            return render(request, 'MainPage/main.html', {'form': form, 'success_message': success_message})
    else:
        form = FileUploadForm()

    return render(request, 'MainPage/main.html', {'form': form})


def recommend(request):
    if request.method == 'POST':
        try:
            # Get the raw JSON data from the request body
            data = json.loads(request.body.decode('utf-8'))

            # Access the data using the keys
            selected_algorithm = data.get('algorithm', '')
            selected_files = data.get('selected_files', '')

            print(f'Selected Algorithm: {selected_algorithm}, Selected Files: {selected_files}')

            request.session['selected_files'] = selected_files
            if selected_algorithm == 'Prefiltering':
                return redirect('prefiltering_page')
            elif selected_algorithm == 'DCR':
                return redirect('DCR_page')
            elif selected_algorithm == 'DCW':
                return redirect('DCW_page')

        except json.JSONDecodeError:
            # Handle JSON decoding error
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    return render(request, 'MainPage/main.html')