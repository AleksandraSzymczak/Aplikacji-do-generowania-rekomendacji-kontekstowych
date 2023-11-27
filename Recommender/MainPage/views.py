from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .forms import FileUploadForm
from django.shortcuts import render, redirect


def home(request):
    return render(request, 'MainPage/main.html')


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
        
        # Przekieruj na odpowiednią stronę w zależności od wyboru
        if selected_algorithm == 'Prefiltering':
            return redirect('prefiltering_page')
        elif selected_algorithm == 'DCR':
            return redirect('DCR_page')
        elif selected_algorithm == 'ItemSplittingKNN':
            return redirect('item_splitting_knn_page')

    return render(request, 'wybor_algorytmu.html')