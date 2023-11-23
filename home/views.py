from django.shortcuts import render
from django.conf import settings

# Create your views here.


def home(request):
    return render(request, 'index.html')


def tournament(request):
    return render(request, 'tournament.html')


def hof(request):
    return render(request, 'hof.html')


def info(request):
    return render(request, "information.html")
