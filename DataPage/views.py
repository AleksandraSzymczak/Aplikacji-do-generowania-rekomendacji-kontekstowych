from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Files
from .forms import FileUploadForm
from django.http import JsonResponse
from django.http import HttpResponse
import json


#@method_decorator(login_required, name='dispatch')
class FileUploadView(View):
    template_name = 'upload_file.html'

    def get(self, request):
        form = FileUploadForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        print(request.user)
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.user = request.user
            file_instance.save_uploaded_file(request.FILES['file_content'])
            file_instance.file_name = request.POST['file_name']
            file_instance.description = request.POST['description']
            file_instance.save()
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
                file_to_delete = Files.objects.get(file_name=file_id, user=request.user)
                print("Deleting file:", file_to_delete)
                file_to_delete.delete()
                deleted_files.append(file_id)
            except Files.DoesNotExist:
                print(f"File not found with id: {file_id}")

        return JsonResponse({'deleted_files': deleted_files})

def Data_page(request):
    current_user = request.user.id
    print(current_user)
    files = Files.objects.filter(user_id=current_user).order_by('-uploaded_at')
    file_des_dict = {file.file_name: file.description for file in files}
    print(file_des_dict)
    return render(request, 'DataPage/data.html', {'pliki_dict': file_des_dict})


class FileDownloadView(View):
    def get(self, request, file_id):
        file_object = get_object_or_404(Files, file_name=file_id, user=request.user)
        response = HttpResponse(file_object.file_content, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file_object.file_name}"'
        return response

def transform(request):
    if request.method == 'POST':
        option_value = request.POST.get('option_value')
        file_Ids = request.POST.get('file_Ids')
        print("OOOOOOOOOOOOOOO")
        if option_value == "binary":
            pass
        if option_value == "compact":
            pass
        if option_value == "loose":
            pass
        response_data = {'message': f'Option clicked: {option_value}'}
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request method'})
