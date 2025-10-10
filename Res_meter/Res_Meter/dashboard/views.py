from django.shortcuts import render
from meters.models import Meter, MeterReading
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from django.shortcuts import redirect
from meters.models import Meter, MeterSpecification

def dashboard_home(request):
    # Get all meters
    meters = Meter.objects.all()
    
    # Count total and active meters
    total_meters = meters.count()
    active_meters = meters.filter(is_active=True).count()
    
    # Calculate total consumption for last 24 hours
    time_24_hours_ago = timezone.now() - timedelta(hours=24)
    total_consumption_24h = MeterReading.objects.filter(
        timestamp__gte=time_24_hours_ago
    ).aggregate(total=Sum('kilowatt_hours'))['total'] or 0
    
    # Add consumption for each meter
    meters_with_consumption = []
    for meter in meters:
        consumption_24h = meter.readings.filter(
            timestamp__gte=time_24_hours_ago
        ).aggregate(total=Sum('kilowatt_hours'))['total'] or 0
        
        meters_with_consumption.append({
            'meter': meter,
            'consumption_24h': consumption_24h
        })
    
    context = {
        'total_meters': total_meters,
        'active_meters': active_meters,
        'total_consumption_24h': total_consumption_24h,
        'meters_with_consumption': meters_with_consumption,
    }
    
    return render(request, 'dashboard/home.html', context)

def meter_detail(request, meter_id):
    meter = Meter.objects.get(id=meter_id)
    
    # Get last 10 readings for this meter
    recent_readings = meter.readings.all()[:10]
    
    # Calculate 24h consumption
    time_24_hours_ago = timezone.now() - timedelta(hours=24)
    consumption_24h = meter.readings.filter(
        timestamp__gte=time_24_hours_ago
    ).aggregate(total=Sum('kilowatt_hours'))['total'] or 0
    
    context = {
        'meter': meter,
        'recent_readings': recent_readings,
        'consumption_24h': consumption_24h,
    }
    
    return render(request, 'dashboard/meter_detail.html', context)


def dashboard_home(request):
    # Get time range from query parameter (default to 24h)
    time_range = request.GET.get('time_range', '24h')
    
    # Calculate time filter based on selection
    now = timezone.now()
    if time_range == '24h':
        time_filter = now - timedelta(hours=24)
    elif time_range == '7d':
        time_filter = now - timedelta(days=7)
    elif time_range == '30d':
        time_filter = now - timedelta(days=30)
    else:  # 'all'
        time_filter = None
    
    # Get all meters
    meters = Meter.objects.all()
    
    # Count total and active meters
    total_meters = meters.count()
    active_meters = meters.filter(is_active=True).count()
    
    # Calculate total consumption based on time range
    if time_filter:
        total_consumption = MeterReading.objects.filter(
            timestamp__gte=time_filter
        ).aggregate(total=Sum('kilowatt_hours'))['total'] or 0
    else:
        total_consumption = MeterReading.objects.aggregate(
            total=Sum('kilowatt_hours'))['total'] or 0
    
    # Add consumption for each meter
    meters_with_consumption = []
    for meter in meters:
        if time_filter:
            consumption = meter.readings.filter(
                timestamp__gte=time_filter
            ).aggregate(total=Sum('kilowatt_hours'))['total'] or 0
        else:
            consumption = meter.readings.aggregate(
                total=Sum('kilowatt_hours'))['total'] or 0
        
        meters_with_consumption.append({
            'meter': meter,
            'consumption': consumption
        })
    
    context = {
        'total_meters': total_meters,
        'active_meters': active_meters,
        'total_consumption': total_consumption,
        'meters_with_consumption': meters_with_consumption,
        'time_range': time_range,
    }
    
    return render(request, 'dashboard/home.html', context)

def add_meter(request):
    if request.method == 'POST':
        # We'll handle form submission here (next step)
        pass
    
    return render(request, 'dashboard/add_meter.html')

def add_meter(request):
    print("View called!")  # Debug
    print("Method:", request.method)  # Debug
    
    if request.method == 'POST':
        print("POST data:", request.POST)  # Debug - see what data we're getting
        
        # Get basic information
        device_id = request.POST.get('device_id')
        name = request.POST.get('name')
        location = request.POST.get('location', '')
        contact_email = request.POST.get('contact_email', '')
        contact_phone = request.POST.get('contact_phone', '')
        description = request.POST.get('description', '')
        
        print(f"Creating meter: {device_id}, {name}")  # Debug
        
        # Create the meter
        meter = Meter.objects.create(
            device_id=device_id,
            name=name,
            location=location,
            contact_email=contact_email,
            contact_phone=contact_phone,
            description=description,
            is_active=True
        )
        
        print("Meter created!")  # Debug
        
        # Get specification data
        capacity = request.POST.get('capacity', '')
        voltage = request.POST.get('voltage', '')
        ampere = request.POST.get('ampere', '')
        additional_specs = request.POST.get('additional_specs', '')
        
        # Get limits
        voltage_upper = request.POST.get('voltage_upper_limit')
        voltage_lower = request.POST.get('voltage_lower_limit')
        ampere_upper = request.POST.get('ampere_upper_limit')
        ampere_lower = request.POST.get('ampere_lower_limit')
        
        # Create specification
        MeterSpecification.objects.create(
            meter=meter,
            capacity=capacity,
            voltage=voltage,
            ampere=ampere,
            additional_specs=additional_specs,
            voltage_upper_limit=voltage_upper if voltage_upper else None,
            voltage_lower_limit=voltage_lower if voltage_lower else None,
            ampere_upper_limit=ampere_upper if ampere_upper else None,
            ampere_lower_limit=ampere_lower if ampere_lower else None,
        )
        
        print("Specification created!")  # Debug
        print("Redirecting...")  # Debug
        
        # Redirect to dashboard after saving
        return redirect('dashboard:home')
    
    return render(request, 'dashboard/add_meter.html')