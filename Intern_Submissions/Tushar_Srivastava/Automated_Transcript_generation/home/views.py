from django.shortcuts import render
from django.http import HttpResponse

def home_view(request):
    context = {'page':'home'}
    return render(request, 'index.html')