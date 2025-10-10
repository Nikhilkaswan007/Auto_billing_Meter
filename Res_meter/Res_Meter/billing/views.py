from django.shortcuts import render, get_object_or_404
from meters.models import Meter
from .models import Invoice

def meter_invoices(request, meter_id):
    meter = get_object_or_404(Meter, id=meter_id)
    invoices = Invoice.objects.filter(meter=meter)
    
    context = {
        'meter': meter,
        'invoices': invoices,
    }
    
    return render(request, 'billing/invoice_list.html', context)

from django.shortcuts import redirect
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum

def create_invoice(request, meter_id):
    meter = get_object_or_404(Meter, id=meter_id)
    
    if request.method == 'POST':
        # Get form data
        period_start = request.POST.get('period_start')
        period_end = request.POST.get('period_end')
        rate_per_kwh = request.POST.get('rate_per_kwh')
        notes = request.POST.get('notes', '')
        
        # Calculate total consumption for the period
        from meters.models import MeterReading
        readings = MeterReading.objects.filter(
            meter=meter,
            timestamp__date__gte=period_start,
            timestamp__date__lte=period_end
        )
        
        total_kwh = readings.aggregate(total=Sum('kilowatt_hours'))['total'] or 0
        
        # Calculate total amount
        total_amount = float(total_kwh) * float(rate_per_kwh)
        
        # Generate invoice number
        import random
        import string
        invoice_number = 'INV-' + ''.join(random.choices(string.digits, k=8))
        
        # Create invoice
        Invoice.objects.create(
            meter=meter,
            invoice_number=invoice_number,
            billing_period_start=period_start,
            billing_period_end=period_end,
            total_kwh=total_kwh,
            rate_per_kwh=rate_per_kwh,
            total_amount=total_amount,
            notes=notes,
            status='draft'
        )
        
        # Redirect to invoice list
        return redirect('billing:meter_invoices', meter_id=meter.id)
    
    return render(request, 'billing/create_invoice.html', {'meter': meter})