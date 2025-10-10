from django.urls import path, include
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('meter/add/', views.add_meter, name='add_meter'),
    path('meter/<int:meter_id>/', views.meter_detail, name='meter_detail'),
     
    
]