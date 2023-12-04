from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .forms import FileUploadForm
from django.shortcuts import render, redirect
from DataPage.views import Files
from django.contrib import messages


def home(request):
    current_user = request.user
    pliki = Files.objects.filter(user=current_user).order_by('-uploaded_at').values_list('file', flat=True)
    substring_to_remove = "user_files/"
    result_list = [full_path.replace(substring_to_remove, "", 1) for full_path in pliki] 
    return render(request, 'MainPage/main.html', {'pliki': result_list})


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
        selected_algorithm = request.POST.get('algorithm', '')
        print(f'Selected Algorithm: {selected_algorithm}')  # Add this line for debugging

        # Przekieruj na odpowiednią stronę w zależności od wyboru
        if selected_algorithm == 'Prefiltering':
            return redirect('prefiltering_page')
        elif selected_algorithm == 'DCR':
            return redirect('DCR_page')
        elif selected_algorithm == 'DCW':
            return redirect('DCW_page')

    return render(request, 'MainPage/main.html')