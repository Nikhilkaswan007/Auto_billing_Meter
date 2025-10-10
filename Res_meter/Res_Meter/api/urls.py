from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('reading/add/', views.add_reading, name='add_reading'),
    path('docs/', views.api_docs, name='docs'),
]
