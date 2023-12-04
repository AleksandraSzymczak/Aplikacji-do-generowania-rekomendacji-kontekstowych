from django.shortcuts import render
from DataPage.views import Files


def data_docs(request):
    return render(request, 'Docs/data_docs.html')

def user_example(request):
    return render(request, 'Docs/user_example.html')
