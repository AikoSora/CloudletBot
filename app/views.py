from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf.urls.static import static
from django.conf import settings

def home(request):
    return render(request, "index.html")