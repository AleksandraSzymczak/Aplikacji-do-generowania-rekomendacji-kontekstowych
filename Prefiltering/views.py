from django.shortcuts import render
from MainPage.models import UploadedFile
import pandas as pd
import logging
from django.http import JsonResponse
from utils.recommendations import Recommender
from DataPage.models import Files
from django.contrib.auth.decorators import login_required
import io

logging.basicConfig(filename="ItemSplit_run.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
 
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def prefiltering_page(request):
    file_param = request.session.get('selected_files')
    print(file_param)
    file_obj = Files.objects.get(file_name=file_param, user=request.user)
    print(file_obj)
    file_content = file_obj.file_content
    file_content_bytesio = io.BytesIO(file_content)

    # Read the BytesIO object into a pandas DataFrame
    df = pd.read_csv(file_content_bytesio)
    col = df.columns
    print(col)
    return render(request, 'Prefiltering/prefiltering_page.html', {"file": file_param})

def Wyniki_prefiltering(request):
    if request.method == 'POST':
        return render(request, 'Prefiltering/prefiltering_results.html')
    return render(request, 'Prefiltering/prefiltering_results.html')



def simulate_long_running_process(request, selected_file):
    print(f"START processing file: {selected_file}")
    logger.info(request)
    file_obj = Files.objects.get(file_name=selected_file, user=request.user)

    if file_obj:
        file_content = file_obj.file_content
        file_content_bytesio = io.BytesIO(file_content)

        # Read the BytesIO object into a pandas DataFrame
        data = pd.read_csv(file_content_bytesio)
        logger.info(data.columns)
        rc_prefiltering = Recommender(data)
        results = rc_prefiltering.perform_calculations()
        logger.info(results)

        # Add any additional logic or response handling as needed
        return JsonResponse({'success': True, 'data': results})
    else:
        logger.warning("No uploaded files found for the current user.")
        return JsonResponse({'success': False, 'error': 'No uploaded files found.'})
