from django.shortcuts import render
from DataPage.views import Files


def data_docs(request):
    return render(request, 'Docs/data_docs.html')

def user_example(request):
    return render(request, 'Docs/user_example.html')

def prefiltering(request):
    return render(request, 'Docs/Prefiltering_doc.html')

def DCR(request):
    return render(request, 'Docs/DCR.html')

def DCW(request):
    return render(request, 'Docs/DCW.html')