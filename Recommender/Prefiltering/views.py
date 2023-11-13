from django.shortcuts import render
from MainPage.models import UploadedFile
import pandas as pd
import logging
from django.http import JsonResponse
from utils.recommendations import Recommender


logging.basicConfig(filename="ItemSplit_run.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
 
logger = logging.getLogger()
logger.setLevel(logging.INFO)


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
    pierwszy_plik = UploadedFile.objects.first()
    file_path = pierwszy_plik.get_file_path()
    data = pd.read_csv(file_path)
    logger.info(data.columns)
    rc_prefiltering = Recommender(data)
    results = rc_prefiltering.perform_calculations()
    logger.info(results)

    return JsonResponse({'result': 'success', 'data': results})