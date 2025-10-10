from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.meter, name='meter'),
    
]