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
        patients = list(Patients.objects.all().values())
        return JsonResponse({'patients': patients})
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
                date_of_birth=data['date_of_birth']
            )
            print("Hasta kaydedildi:", patient)
            return JsonResponse({'success': True})
        except Exception as e:
            print("HATA:", e)
            return JsonResponse({'success': False, 'error': str(e)}, status=500)