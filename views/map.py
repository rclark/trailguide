from trailguide.utils import HttpResponseNotImplemented
from django.shortcuts import render

def map_page(request):
    return render(request, "trailguide/map.html")