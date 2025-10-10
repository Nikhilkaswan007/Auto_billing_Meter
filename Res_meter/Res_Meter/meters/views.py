from django.shortcuts import render,HttpResponse

# Create your views here.
def meter(request):
    return HttpResponse("Hello, this is the meter view.")
