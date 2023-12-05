from django.conf import settings
from django.shortcuts import render, redirect
from MainPage.models import UploadedFile
from .forms import UserChoicesForm
import pandas as pd
import json
import logging
from DataPage.models import Files
from utils.recommendations import Recommender
from django.http import JsonResponse


logging.basicConfig(filename="ItemSplit_run.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
 
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def DCW_page(request):
    file_param = request.session.get('selected_files')
    file_obj = Files.objects.get(file=f"user_files/{file_param}", user=request.user)
    df = pd.read_csv(file_obj.file.path)
    context_var_list = df.columns[3:].values.tolist()
    return render(request, 'DCW/dcw_page.html', {'context_list': context_var_list})


def Wyniki_DCW(request):
    if request.method == 'POST':
        weights_dict = request.POST.get('hidden_values', '{}')
        
        c1_choices_list = request.POST.getlist('c1_choices')
        c2_choices_list = request.POST.getlist('c2_choices')
        c3_choices_list = request.POST.getlist('c3_choices')

        weights_json = json.loads(weights_dict)

        c1_choices_json = json.dumps(c1_choices_list)
        c2_choices_json = json.dumps(c2_choices_list)
        c3_choices_json = json.dumps(c3_choices_list)
        form_data = {
            'c1_choices': c1_choices_json,
            'c2_choices': c2_choices_json,
            'c3_choices': c3_choices_json,
            'weights': weights_json
        }
        form = UserChoicesForm(form_data)

        if form.is_valid():
            request.session['form_data'] = form_data
            form.save()
    else:
        form = UserChoicesForm()

    return render(request, 'DCW/dcw_results.html', {'form': form, 'weights': weights_json})