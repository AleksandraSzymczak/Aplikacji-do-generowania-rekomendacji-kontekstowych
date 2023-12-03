from django.shortcuts import render
from MainPage.models import UploadedFile
import pandas as pd
import logging
from django.http import JsonResponse
from utils.recommendations import Recommender
from DataPage.models import Files
from django.contrib.auth.decorators import login_required


logging.basicConfig(filename="ItemSplit_run.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
 
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def prefiltering_page(request):
    #pierwszy_plik = UploadedFile.objects.first()
    #file_path = pierwszy_plik.get_file_path()
    #df = pd.read_csv(file_path) 
    #column_list = df.columns
    return render(request, 'Prefiltering/prefiltering_page.html', {'context_list': "column_list"})


def Wyniki_prefiltering(request):
    if request.method == 'POST':
        return render(request, 'Prefiltering/prefiltering_results.html')
    return render(request, 'Prefiltering/prefiltering_results.html')


@login_required
def simulate_long_running_process(request):
    logger.info("START")
    logger.info(request)
    current_user = request.user
    ostatni_plik = Files.objects.filter(user=current_user).order_by('-uploaded_at').first()

    if ostatni_plik:
        file_path = ostatni_plik.file.path
        data = pd.read_csv(file_path)
        logger.info(data.columns)
        rc_prefiltering = Recommender(data)
        results = rc_prefiltering.perform_calculations()
        logger.info(results)

        # Add any additional logic or response handling as needed
        return JsonResponse({'success': True, 'data': results})
    else:
        logger.warning("No uploaded files found for the current user.")
        return JsonResponse({'success': False, 'error': 'No uploaded files found.'})
