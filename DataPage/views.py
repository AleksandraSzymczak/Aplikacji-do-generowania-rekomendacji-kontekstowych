# W twoim pliku views.py

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Files
from .forms import FileUploadForm
from django.http import JsonResponse
from django.http import FileResponse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import pandas as pd
from django.http import JsonResponse
import json


@method_decorator(login_required, name='dispatch')
class FileUploadView(View):
    template_name = 'upload_file.html'

    def get(self, request):
        form = FileUploadForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = FileUploadForm(request.POST, request.FILES)
        print(request.FILES)
        print(form.errors)
        if form.is_valid():
            new_file = form.save(commit=False)
            new_file.user = request.user
            new_file.description = request.POST.get('description')
            new_file.save()
            return redirect('Data_page')
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

@method_decorator(login_required, name='dispatch')
class FileDeleteView(View):
    def post(self, request):
        try:
            file_ids = json.loads(request.body.decode('utf-8'))['file_ids']
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

        print("User:", request.user)
        deleted_files = []

        for file_id in file_ids:
            try:
                # Attempt to convert file_id to integer
                #file_id = int(file_id)
                file_to_delete = Files.objects.get(file="user_files/"+file_id, user=request.user)
                print("Deleting file:", file_to_delete)
                file_to_delete.delete()
                deleted_files.append(file_id)
            except ValueError:
                print(f"Invalid file_id: {file_id}")
                # Handle the case where file_id is not a valid integer

        return JsonResponse({'deleted_files': deleted_files})


def Data_page(request):
    current_user = request.user
    pliki = Files.objects.filter(user=current_user).order_by('-uploaded_at').values_list('file', flat=True)
    substring_to_remove = "user_files/"
    result_list = [full_path.replace(substring_to_remove, "", 1) for full_path in pliki] 
    return render(request, 'DataPage/data.html', {'pliki': result_list})


class FileDownloadView(View):
    def get(self, request, file_id):
        file_object = get_object_or_404(Files, file="user_files/"+file_id, user=request.user)
        file_path = file_object.file.path  # Assuming 'file' is a FileField in your model
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{file_object.file.name}"'
            return response

def transform(request):
    if request.method == 'POST':
        option_value = request.POST.get('option_value')
        file_Ids = request.POST.get('file_Ids')
        if option_value == "binary":
            pass
        if option_value == "comact":
            pass
        if option_value == "loose":
            pass
        response_data = {'message': f'Option clicked: {option_value}'}
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request method'})