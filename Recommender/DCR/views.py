from django.conf import settings
from django.shortcuts import render, redirect
from MainPage.models import UploadedFile
from .forms import UserChoicesForm
import pandas as pd


def DCR_page(request):
    pierwszy_plik = UploadedFile.objects.first()
    file_path = pierwszy_plik.get_file_path()
    df = pd.read_csv(file_path) 
    context_var_list = df.columns[3:].tolist()
    return render(request, 'DCR/dcr_page.html', {'context_list': context_var_list})


def Wyniki(request):
    if request.method == 'POST':
        form = UserChoicesForm(request.POST)
        if form.is_valid():
            user_choices = form.save()
            return render(request, 'DCR/dcr_results.html', {'user_choices': user_choices})
        else:
            print(form.errors)  # Wypisz błędy walidacji formularza
    return render(request, 'DCR/dcr_results.html', {'user_choices': None})