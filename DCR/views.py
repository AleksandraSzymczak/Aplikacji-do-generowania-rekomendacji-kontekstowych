from django.conf import settings
from django.shortcuts import render, redirect
from MainPage.models import UploadedFile
from .forms import UserChoicesForm
import pandas as pd
import json
import logging
from utils.recommendations import Recommender
from django.http import JsonResponse


logging.basicConfig(filename="ItemSplit_run.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
 
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def DCR_page(request):
    return render(request, 'DCR/dcr_page.html', {'context_list': ["context_var_list"]})


def Wyniki(request):
    if request.method == 'POST':
        c1_choices_list = request.POST.getlist('c1_choices')
        c2_choices_list = request.POST.getlist('c2_choices')
        c3_choices_list = request.POST.getlist('c3_choices')

        c1_choices_json = json.dumps(c1_choices_list)
        c2_choices_json = json.dumps(c2_choices_list)
        c3_choices_json = json.dumps(c3_choices_list)
        form_data = {
            'c1_choices': c1_choices_json,
            'c2_choices': c2_choices_json,
            'c3_choices': c3_choices_json,
        }

        form = UserChoicesForm(form_data)

        if form.is_valid():
            request.session['form_data'] = form_data
            form.save()
    else:
        form = UserChoicesForm()

    return render(request, 'DCR/dcr_results.html', {'form': form})


def simulate_long_running_process(request):
    form_data = request.session.get('form_data', {})
    pierwszy_plik = UploadedFile.objects.first()
    file_path = pierwszy_plik.get_file_path()
    data = pd.read_csv(file_path)
    logger.info(form_data)
    rc_prefiltering = Recommender(data, type="DCR", form_data=form_data)
    results = rc_prefiltering.perform_calculations()
    logger.info(results)

    return JsonResponse({'result': 'success', 'data': results})