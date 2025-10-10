from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('meter/<int:meter_id>/invoices/', views.meter_invoices, name='meter_invoices'),
    path('meter/<int:meter_id>/create/', views.create_invoice, name='create_invoice'),
]