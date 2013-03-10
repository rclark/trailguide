from trailguide.utils import HttpResponseNotImplemented
from django.shortcuts import render

def home_page(request):
    return render(request, "trailguide/home.html")