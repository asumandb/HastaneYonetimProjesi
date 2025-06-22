from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from ..models.beds_model import Beds

def beds_view(request):
    beds = Beds.objects.all()
    return render(request, 'beds.html', {'beds': beds, 'title': 'Yataklar'})

def bed_create(request):
    if request.method == 'POST':
        number = request.POST.get('number')
        room = request.POST.get('room')
        status = request.POST.get('status')
        if number and room and status:
            bed = Beds.objects.create(number=number, room=room, status=status)
            return JsonResponse({'success': True, 'bed': {'id': bed.id, 'number': bed.number, 'room': bed.room, 'status': bed.status}})
        else:
            return JsonResponse({'success': False, 'error': 'Tüm alanlar zorunludur.'})
    return JsonResponse({'success': False, 'error': 'Sadece POST isteği desteklenir.'})

def bed_update(request, bed_id):
    bed = get_object_or_404(Beds, id=bed_id)
    if request.method == 'POST':
        number = request.POST.get('number')
        room = request.POST.get('room')
        status = request.POST.get('status')
        if number and room and status:
            bed.number = number
            bed.room = room
            bed.status = status
            bed.save()
            return JsonResponse({'success': True, 'bed': {'id': bed.id, 'number': bed.number, 'room': bed.room, 'status': bed.status}})
        else:
            return JsonResponse({'success': False, 'error': 'Tüm alanlar zorunludur.'})
    return JsonResponse({'success': False, 'error': 'Sadece POST isteği desteklenir.'})

def bed_delete(request, bed_id):
    bed = get_object_or_404(Beds, id=bed_id)
    if request.method == 'POST':
        bed.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Sadece POST isteği desteklenir.'})
