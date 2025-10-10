from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from meters.models import Meter, MeterReading
import json

@csrf_exempt
def add_reading(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from Raspberry Pi
            data = json.loads(request.body)
            
            device_id = data.get('device_id')
            kilowatt_hours = data.get('kilowatt_hours')
            current_voltage = data.get('voltage')
            current_ampere = data.get('ampere')
            
            # Find the meter by device_id
            meter = Meter.objects.get(device_id=device_id)
            
            # Create the reading
            reading = MeterReading.objects.create(
                meter=meter,
                kilowatt_hours=kilowatt_hours,
                current_voltage=current_voltage,
                current_ampere=current_ampere
            )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Reading saved successfully',
                'reading_id': reading.id
            })
            
        except Meter.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Meter not found'
            }, status=404)
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Only POST method allowed'
    }, status=405)

def api_docs(request):
    from django.shortcuts import render
    return render(request, 'api/docs.html')