from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from ..models.prescriptions_model import Prescriptions
from ..models.appointments_model import Appointment
from ..models.patients_model import Patients
from ..models.doctors_model import Doctors
from ..models.clinic_model import Clinic
import json

def prescriptions_view(request):
    return render(request, 'prescriptions.html')

@require_http_methods(["GET"])
def api_appointments(request):
    # Hasta, doktor, poliklinik bilgileriyle birlikte randevuları döndür
    appointments = Appointment.objects.select_related('patient', 'doctor', 'doctor__clinic').all()
    data = []
    for a in appointments:
        data.append({
            'id': a.id,
            'patient': f"{a.patient.name} {a.patient.surname}",
            'doctor': f"{a.doctor.name} {a.doctor.surname}",
            'clinic': a.doctor.clinic.name,
            'date': str(a.date),
            'time': str(a.time),
        })
    return JsonResponse(data, safe=False)

@require_http_methods(["GET"])
def api_prescriptions(request):
    # Reçeteleri hasta, doktor, poliklinik ve tarih ile döndür
    prescriptions = Prescriptions.objects.select_related('appointment', 'appointment__patient', 'appointment__doctor', 'appointment__doctor__clinic').all().order_by('-id')
    data = []
    for p in prescriptions:
        data.append({
            'id': p.id,
            'patient': f"{p.appointment.patient.name} {p.appointment.patient.surname}",
            'doctor': f"{p.appointment.doctor.name} {p.appointment.doctor.surname}",
            'clinic': p.appointment.doctor.clinic.name,
            'date': str(p.appointment.date),
            'time': str(p.appointment.time),
            'medicine': p.medicine,
        })
    return JsonResponse(data, safe=False)

@csrf_exempt
@require_http_methods(["POST"])
def api_add_prescription(request):
    data = json.loads(request.body.decode())
    appointment_id = data.get('appointment_id')
    medicine = data.get('medicine')
    if not appointment_id or not medicine:
        return JsonResponse({'error': 'Eksik bilgi.'}, status=400)
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        prescription = Prescriptions.objects.create(appointment=appointment, medicine=medicine)
        return JsonResponse({'success': True, 'id': prescription.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
