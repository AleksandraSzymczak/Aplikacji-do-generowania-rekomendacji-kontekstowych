from django.shortcuts import render
from DataPage.views import Files
from django.contrib.auth.decorators import login_required

@login_required
def data_docs(request):
    return render(request, 'Docs/data_docs.html')

@login_required
def user_example(request):
    return render(request, 'Docs/user_example.html')

@login_required
def prefiltering(request):
    return render(request, 'Docs/Prefiltering_doc.html')

@login_required
def DCR(request):
    return render(request, 'Docs/DCR.html')

@login_required
def DCW(request):
    return render(request, 'Docs/DCW.html')