from django.shortcuts import render
from hastane.models import Patients
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def patient_registration_view(request):
    patients = Patients.objects.all()
    return render(request, 'patient_registration.html') 

@csrf_exempt  # Sadece test için, güvenlik için CSRF token ile kullanmak daha iyidir!
def patient_list(request):
    if request.method == 'GET':
        patients = Patients.objects.all()
        data = []
        for p in patients:
            data.append({
                'id': p.id,
                'name': p.name,
                'surname': p.surname,
                'email': p.email,
                'phone': p.phone,
                'tc_number': p.tc_number,
                'date_of_birth': str(p.date_of_birth) if p.date_of_birth else '',
                'entry_date': str(p.entry_date) if p.entry_date else '',
                'exit_date': str(p.exit_date) if p.exit_date else ''
            })
        return JsonResponse({'patients': data})
    elif request.method == 'POST':
        try:
            print("POST isteği geldi!")
            print("request.body:", request.body)
            data = json.loads(request.body)
            print("Gelen data:", data)
            patient = Patients.objects.create(
                name=data['name'],
                surname=data['surname'],
                email=data['email'],
                phone=data['phone'],
                tc_number=data['tc_number'],
                date_of_birth=data['date_of_birth'],
                entry_date=data.get('entry_date'),
                exit_date=data.get('exit_date')
            )
            print("Hasta kaydedildi:", patient)
            return JsonResponse({'success': True})
        except Exception as e:
            print("HATA:", e)
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
def patient_update(request, patient_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            patient = Patients.objects.get(id=patient_id)
            patient.name = data['name']
            patient.surname = data['surname']
            patient.email = data['email']
            patient.phone = data['phone']
            patient.tc_number = data['tc_number']
            patient.date_of_birth = data['date_of_birth']
            # Giriş/çıkış tarihi de ekle:
            patient.entry_date = data.get('entry_date')
            patient.exit_date = data.get('exit_date')
            patient.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
def patient_delete(request, patient_id):
    if request.method == 'POST':
        try:
            patient = Patients.objects.get(id=patient_id)
            patient.delete()
            return JsonResponse({'success': True})
        except Patients.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Hasta bulunamadı.'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Geçersiz istek yöntemi'}, status=405)