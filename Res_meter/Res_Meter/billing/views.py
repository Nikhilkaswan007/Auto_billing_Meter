from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from io import BytesIO
from django.shortcuts import render, get_object_or_404
from meters.models import Meter
from .models import Invoice
from django.core.mail import EmailMessage

@login_required
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

@login_required
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

@login_required
def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    context = {
        'invoice': invoice,
    }
    
    return render(request, 'billing/invoice_detail.html', context)

@login_required
def download_invoice_pdf(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    # Create a file buffer
    buffer = BytesIO()
    
    # Create PDF
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f2937'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    # Title
    title = Paragraph(f"INVOICE {invoice.invoice_number}", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))
    
    # Invoice Info
    invoice_data = [
        ['Invoice Date:', invoice.created_at.strftime('%B %d, %Y')],
        ['Billing Period:', f"{invoice.billing_period_start.strftime('%b %d, %Y')} - {invoice.billing_period_end.strftime('%b %d, %Y')}"],
        ['Status:', invoice.get_status_display()],
    ]
    
    invoice_table = Table(invoice_data, colWidths=[2*inch, 3*inch])
    invoice_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elements.append(invoice_table)
    elements.append(Spacer(1, 0.4*inch))
    
    # Customer Details
    customer_title = Paragraph("<b>CUSTOMER DETAILS</b>", styles['Heading2'])
    elements.append(customer_title)
    elements.append(Spacer(1, 0.2*inch))
    
    customer_data = [
        ['Meter Name:', invoice.meter.name],
        ['Location:', invoice.meter.location or 'N/A'],
        ['Email:', invoice.meter.contact_email or 'N/A'],
        ['Phone:', invoice.meter.contact_phone or 'N/A'],
    ]
    
    customer_table = Table(customer_data, colWidths=[2*inch, 3*inch])
    customer_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elements.append(customer_table)
    elements.append(Spacer(1, 0.4*inch))
    
    # Billing Summary
    billing_title = Paragraph("<b>BILLING SUMMARY</b>", styles['Heading2'])
    elements.append(billing_title)
    elements.append(Spacer(1, 0.2*inch))
    
    billing_data = [
        ['Description', 'Quantity', 'Rate', 'Amount'],
        ['Electricity Consumption', f"{invoice.total_kwh} kWh", f"₹{invoice.rate_per_kwh}", f"₹{invoice.total_amount}"],
    ]
    
    billing_table = Table(billing_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    billing_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
    ]))
    
    elements.append(billing_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Total
    total_style = ParagraphStyle(
        'Total',
        parent=styles['Normal'],
        fontSize=16,
        textColor=colors.HexColor('#1f2937'),
        alignment=TA_RIGHT,
        fontName='Helvetica-Bold'
    )
    total = Paragraph(f"<b>TOTAL AMOUNT: ₹{invoice.total_amount}</b>", total_style)
    elements.append(total)
    
    # Notes
    if invoice.notes:
        elements.append(Spacer(1, 0.4*inch))
        notes_title = Paragraph("<b>NOTES:</b>", styles['Heading3'])
        elements.append(notes_title)
        elements.append(Spacer(1, 0.1*inch))
        notes = Paragraph(invoice.notes, styles['Normal'])
        elements.append(notes)
    
    # Build PDF
    doc.build(elements)
    
    # Get PDF from buffer
    pdf = buffer.getvalue()
    buffer.close()
    
    # Create response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.invoice_number}.pdf"'
    response.write(pdf)
    
    return response

@login_required
def send_invoice_email(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    if request.method == 'POST':
        recipient_email = request.POST.get('recipient_email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        try:
            # Create email
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=None,  # Uses DEFAULT_FROM_EMAIL from settings
                to=[recipient_email],
            )
            
            # Generate PDF and attach it
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []
            
            # Build PDF (same code as download function)
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1f2937'),
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            title = Paragraph(f"INVOICE {invoice.invoice_number}", title_style)
            elements.append(title)
            elements.append(Spacer(1, 0.3*inch))
            
            invoice_data = [
                ['Invoice Date:', invoice.created_at.strftime('%B %d, %Y')],
                ['Billing Period:', f"{invoice.billing_period_start.strftime('%b %d, %Y')} - {invoice.billing_period_end.strftime('%b %d, %Y')}"],
                ['Status:', invoice.get_status_display()],
            ]
            
            invoice_table = Table(invoice_data, colWidths=[2*inch, 3*inch])
            invoice_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            
            elements.append(invoice_table)
            elements.append(Spacer(1, 0.4*inch))
            
            customer_title = Paragraph("<b>CUSTOMER DETAILS</b>", styles['Heading2'])
            elements.append(customer_title)
            elements.append(Spacer(1, 0.2*inch))
            
            customer_data = [
                ['Meter Name:', invoice.meter.name],
                ['Location:', invoice.meter.location or 'N/A'],
                ['Email:', invoice.meter.contact_email or 'N/A'],
                ['Phone:', invoice.meter.contact_phone or 'N/A'],
            ]
            
            customer_table = Table(customer_data, colWidths=[2*inch, 3*inch])
            customer_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            
            elements.append(customer_table)
            elements.append(Spacer(1, 0.4*inch))
            
            billing_title = Paragraph("<b>BILLING SUMMARY</b>", styles['Heading2'])
            elements.append(billing_title)
            elements.append(Spacer(1, 0.2*inch))
            
            billing_data = [
                ['Description', 'Quantity', 'Rate', 'Amount'],
                ['Electricity Consumption', f"{invoice.total_kwh} kWh", f"₹{invoice.rate_per_kwh}", f"₹{invoice.total_amount}"],
            ]
            
            billing_table = Table(billing_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
            billing_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
            ]))
            
            elements.append(billing_table)
            elements.append(Spacer(1, 0.3*inch))
            
            total_style = ParagraphStyle(
                'Total',
                parent=styles['Normal'],
                fontSize=16,
                textColor=colors.HexColor('#1f2937'),
                alignment=TA_RIGHT,
                fontName='Helvetica-Bold'
            )
            total = Paragraph(f"<b>TOTAL AMOUNT: ₹{invoice.total_amount}</b>", total_style)
            elements.append(total)
            
            if invoice.notes:
                elements.append(Spacer(1, 0.4*inch))
                notes_title = Paragraph("<b>NOTES:</b>", styles['Heading3'])
                elements.append(notes_title)
                elements.append(Spacer(1, 0.1*inch))
                notes = Paragraph(invoice.notes, styles['Normal'])
                elements.append(notes)
            
            doc.build(elements)
            
            # Attach PDF
            pdf = buffer.getvalue()
            buffer.close()
            email.attach(f'invoice_{invoice.invoice_number}.pdf', pdf, 'application/pdf')
            
            # Send email
            email.send()
            
            # Update invoice status
            invoice.status = 'sent'
            invoice.sent_at = timezone.now()
            invoice.save()
            
            # Success message - redirect back to invoice
            return redirect('billing:invoice_detail', invoice_id=invoice.id)
            
        except Exception as e:
            # For now, print error and redirect
            print(f"Error sending email: {e}")
            return redirect('billing:invoice_detail', invoice_id=invoice.id)
    
    # Prepare email template
    context = {
        'invoice': invoice,
        'default_subject': f'Invoice {invoice.invoice_number} - {invoice.meter.name}',
        'default_message': f'''Dear Customer,

Please find attached your electricity bill for the period {invoice.billing_period_start.strftime('%B %d, %Y')} to {invoice.billing_period_end.strftime('%B %d, %Y')}.

Invoice Details:
- Invoice Number: {invoice.invoice_number}
- Consumption: {invoice.total_kwh} kWh
- Amount Due: ₹{invoice.total_amount}

Thank you for your business.

Best regards,
Energy Meter Billing System''',
    }
    
    return render(request, 'billing/send_email.html', context)

@login_required
def send_invoice_sms(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    if request.method == 'POST':
        # Get form data
        recipient_phone = request.POST.get('recipient_phone')
        message = request.POST.get('message')
        
        # For now, just mark as sent (you can integrate SMS API later)
        if invoice.status == 'draft':
            invoice.status = 'sent'
            invoice.sent_at = timezone.now()
            invoice.save()
        
        return redirect('billing:invoice_detail', invoice_id=invoice.id)
    
    # Prepare SMS template
    context = {
        'invoice': invoice,
        'default_message': f'''Invoice {invoice.invoice_number}
Meter: {invoice.meter.name}
Period: {invoice.billing_period_start.strftime('%d/%m/%Y')} - {invoice.billing_period_end.strftime('%d/%m/%Y')}
Consumption: {invoice.total_kwh} kWh
Amount Due: ₹{invoice.total_amount}
Please make payment at the earliest. Thank you!''',
    }
    
    return render(request, 'billing/send_sms.html', context)

@login_required
def update_invoice_status(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        invoice.status = new_status
        invoice.save()
        
        return redirect('billing:invoice_detail', invoice_id=invoice.id)
    
    return redirect('billing:invoice_detail', invoice_id=invoice.id)