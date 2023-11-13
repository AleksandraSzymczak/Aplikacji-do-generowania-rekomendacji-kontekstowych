from django.shortcuts import render
from MainPage.models import UploadedFile
import pandas as pd
from tqdm import tqdm
import time
from django.http import JsonResponse


def prefiltering_page(request):
    pierwszy_plik = UploadedFile.objects.first()
    file_path = pierwszy_plik.get_file_path()
    df = pd.read_csv(file_path) 
    column_list = df.columns
    return render(request, 'Prefiltering/prefiltering_page.html', {'context_list': column_list})


def Wyniki_prefiltering(request):
    if request.method == 'POST':
        return render(request, 'Prefiltering/prefiltering_results.html')
    return render(request, 'Prefiltering/prefiltering_results.html')


def simulate_long_running_process(request):
    data = []
    for i in tqdm(range(100), desc="Processing"):
        time.sleep(0.1)
        data.append(f"Step {i} completed.")

    return JsonResponse({'result': 'success', 'data': data})