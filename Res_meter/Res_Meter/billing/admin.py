from django.contrib import admin
from .models import Invoice

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'meter', 'total_kwh', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['invoice_number', 'meter__name']

admin.site.register(Invoice, InvoiceAdmin)
