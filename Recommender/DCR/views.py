from django.conf import settings
from django.shortcuts import render
from MainPage.models import UploadedFile
import pandas as pd


def DCR_page(request):
    pierwszy_plik = UploadedFile.objects.first()
    file_path = pierwszy_plik.get_file_path()
    df = pd.read_csv(file_path) 
    context_var_list = df.columns[3:].tolist()
    return render(request, 'DCR/DCR_page.html', {'context_list': context_var_list})
