from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from meters.models import Meter, MeterReading
import json
from meters.models import MeterCommand

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

@csrf_exempt
def get_pending_commands(request, device_id):

    if request.method == 'GET':
        try:
            # Find meter by device_id
            meter = Meter.objects.get(device_id=device_id)
            
            # Get all pending commands for this meter
            pending_commands = MeterCommand.objects.filter(
                meter=meter,
                status='pending'
            )
            
            # Convert to list
            commands_list = []
            for cmd in pending_commands:
                commands_list.append({
                    'command_id': cmd.id,
                    'command': cmd.command,
                    'created_at': cmd.created_at.isoformat(),
                })
            
            return JsonResponse({
                'status': 'success',
                'device_id': device_id,
                'commands': commands_list
            })
            
        except Meter.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Meter not found'
            }, status=404)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Only GET method allowed'
    }, status=405)

@csrf_exempt
def update_command_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            command_id = data.get('command_id')
            status = data.get('status')  # 'executed' or 'failed'
            
            # Find and update command
            command = MeterCommand.objects.get(id=command_id)
            command.status = status
            
            if status == 'executed':
                from django.utils import timezone
                command.executed_at = timezone.now()
            
            command.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Command status updated',
                'command_id': command_id,
                'new_status': status
            })
            
        except MeterCommand.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Command not found'
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


