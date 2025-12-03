from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('meter/<int:meter_id>/invoices/', views.meter_invoices, name='meter_invoices'),
    path('meter/<int:meter_id>/create/', views.create_invoice, name='create_invoice'),
    path('invoice/<int:invoice_id>/', views.invoice_detail, name='invoice_detail'),
    path('invoice/<int:invoice_id>/pdf/', views.download_invoice_pdf, name='download_pdf'),
    path('invoice/<int:invoice_id>/email/', views.send_invoice_email, name='send_email'),
    path('invoice/<int:invoice_id>/sms/', views.send_invoice_sms, name='send_sms'),
    path('invoice/<int:invoice_id>/status/', views.update_invoice_status, name='update_status'),
    
]