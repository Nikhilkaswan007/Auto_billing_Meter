from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
# Create your views here.
def meter(request):
    return HttpResponse("Hello, this is the meter view.")
