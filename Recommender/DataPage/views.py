# W twoim pliku views.py

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Files
from .forms import FileUploadForm
from django.http import JsonResponse


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
            new_file.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

@method_decorator(login_required, name='dispatch')
class FileDeleteView(View):
    template_name = 'delete_file.html'

    def get(self, request, file_id):
        file_to_delete = Files.objects.get(id=file_id)
        return render(request, self.template_name, {'file': file_to_delete})

    def post(self, request, file_id):
        file_to_delete = Files.objects.get(id=file_id)
        file_to_delete.delete()
        return redirect('home')  # Przekieruj na stronę główną po usunięciu pliku
