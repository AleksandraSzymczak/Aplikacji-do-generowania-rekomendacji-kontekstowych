from django.shortcuts import render
from MainPage.models import UploadedFile
import pandas as pd
import logging
from django.http import JsonResponse
from DataPage.models import Files
from django.contrib.auth.decorators import login_required
import io
from django.contrib.auth.decorators import login_required
from utils.data_utils import handle_recommender
from utils.data_cleaning.utils import scale_ratings, z_score_normalisation

from surprise import Dataset, Reader, accuracy
from surprise.model_selection import KFold
from surprise.prediction_algorithms.knns import KNNWithMeans

from django.http import StreamingHttpResponse
import time

logging.basicConfig(filename="ItemSplit_run.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
 
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def log_stream(request):
    def event_stream():
        log_path = f'ItemSplit_run.log'  # Ustaw ścieżkę do twojego pliku log.txt

        with open(log_path, 'r') as log_file:
            while True:
                line = log_file.readline()
                if not line:
                    time.sleep(0.01)  # Jeśli nie ma nowej linii, czekaj przez 1 sekundę i spróbuj ponownie
                    continue

                yield f"data: {line}\n\n"

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response['Cache-Control'] = 'no-cache'
    return response


@login_required
def collaborative_filtering_page(request):
    file_param = request.session.get('selected_files')
    print(file_param)
    file_obj = Files.objects.get(file_name=file_param, user=request.user)
    print(file_obj)
    file_content = file_obj.file_content
    file_content_bytesio = io.BytesIO(file_content)

    df = pd.read_csv(file_content_bytesio)
    col = df.columns
    print(col)
    return render(request, 'Prefiltering/prefiltering_page.html', {"file": file_param})


@login_required
def Wyniki_collaborative_filtering(request):
    if request.method == 'POST':
        return render(request, 'Prefiltering/prefiltering_results.html')
    return render(request, 'Prefiltering/prefiltering_results.html')


@login_required
def simulate_long_running_process(request, selected_file):
    print(f"START processing file: {selected_file}")
    logger.info(request)
    file_obj = Files.objects.get(file_name=selected_file, user=request.user)
    kfold_value = int(request.GET.get('KFold', 2))
    maxValue = int(request.GET.get('maxValue'), 0)
    minValue = int(request.GET.get('minValue'), 0)
    cleanup_data = request.GET.get('cleanup_data')
    Zscore = request.GET.get('Zscore')

    if file_obj:
        file_content = file_obj.file_content
        file_content_bytesio = io.BytesIO(file_content)

        data = pd.read_csv(file_content_bytesio)
        logger.info(data.columns)
        USER_COL, ITEM_COL, RATING = data.iloc[:, :3]
        data[RATING] = data[RATING].astype(int)
        if cleanup_data:
            data[data.duplicated(subset=[USER_COL, ITEM_COL], keep='first')]
            logger.info("Duplicates dropped")

        if Zscore:
            outliers = z_score_normalisation(data[RATING], 3)
            data['Outlier'] = outliers
            data = data[~outliers]
            data = data.drop('Outlier', axis=1)
            logger.info("Zscore normalisation applied")

        if maxValue != 0 and minValue != 0:
            data[RATING] = scale_ratings(data[RATING], minValue, maxValue)
            logger.info(f"Rating column scaled - MIN:{minValue}, MAX:{maxValue}")


        n_splits = kfold_value
        reader = Reader(rating_scale=(1, 10))
        data = Dataset.load_from_df(data[[USER_COL, ITEM_COL, RATING]], reader)
        kf = KFold(n_splits=n_splits)
        logger.info("data splitting")
        algo = KNNWithMeans(k=40, min_k=1, sim_options={"user_based":True}, verbose=True)
        results = {
            "rmse": [],
            "mae": [],
            "mse": []
        }
        for trainset, testset in kf.split(data):
            algo.fit(trainset)
            predictions = algo.test(testset)
            results["rmse"].append(accuracy.rmse(predictions, verbose=True))
            results["mae"].append(accuracy.mae(predictions, verbose=True))
            results["mse"].append(accuracy.mse(predictions, verbose=True))
        return JsonResponse({'success': True, 'data': results})
    else:
        logger.warning("No uploaded files found for the current user.")
        return JsonResponse({'success': False, 'error': 'No uploaded files found.'})
