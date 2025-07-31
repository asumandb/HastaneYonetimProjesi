from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from ..models.rooms_model import Rooms
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError

def room_list(request):
    # Tüm odaları listele
    rooms = Rooms.objects.all()
    return render(request, 'rooms.html', {'rooms': rooms, 'title': 'Odalar'})

@csrf_exempt
@require_POST
def add_room(request):
    room_type = request.POST.get('room_type')
    status = request.POST.get('status')
    description = request.POST.get('description')
    number = request.POST.get('number')
    if number and room_type and status:
        try:
            room = Rooms.objects.create(number=number, room_type=room_type, status=status, description=description)
            return JsonResponse({'success': True, 'room': {'id': room.id, 'number': room.number, 'room_type': room.room_type, 'status': room.status, 'description': room.description}})
        except IntegrityError:
            return JsonResponse({'success': False, 'error': 'Bu oda numarası zaten kayıtlı!'})
    else:
        return JsonResponse({'success': False, 'error': 'Tüm alanlar zorunludur.'})

@csrf_exempt
@require_POST
def update_room(request, room_id):
    room = get_object_or_404(Rooms, id=room_id)
    number = request.POST.get('number')
    room_type = request.POST.get('room_type')
    status = request.POST.get('status')
    description = request.POST.get('description')
    if number and room_type and status:
        # Başka bir odada aynı numara var mı kontrol et
        if Rooms.objects.exclude(id=room_id).filter(number=number).exists():
            return JsonResponse({'success': False, 'error': 'Bu oda numarası zaten kayıtlı!'})
        room.number = number
        room.room_type = room_type
        room.status = status
        room.description = description
        room.save()
        return JsonResponse({'success': True, 'room': {'id': room.id, 'number': room.number, 'room_type': room.room_type, 'status': room.status, 'description': room.description}})
    else:
        return JsonResponse({'success': False, 'error': 'Tüm alanlar zorunludur.'})

@csrf_exempt
@require_POST
def delete_room(request, room_id):
    room = get_object_or_404(Rooms, id=room_id)
    room.delete()
    return JsonResponse({'success': True})

@require_GET
def room_description(request, room_id):
    room = get_object_or_404(Rooms, id=room_id)
    description = getattr(room, 'description', None) or f"Oda {room.number} - Tip: {room.room_type} - Durum: {room.status}"
    return JsonResponse({'description': description})

@require_GET
def room_dropdown(request):
    # Dropdown için benzersiz oda listesini döner
    rooms = Rooms.objects.all()
    room_list = [{'id': room.id, 'number': room.number} for room in rooms]
    return JsonResponse({'rooms': room_list})