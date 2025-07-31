from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
import json

from hastane.models.clinic_model import Clinic
from hastane.models.doctors_model import Doctors
from hastane.models.appointments_model import Appointment
from hastane.models.patients_model import Patients

def take_appointments_view(request):
    """
    Randevu alma sayfası view'ı
    GET: Formu gösterir
    POST: Randevu oluşturur
    """
    if request.method == 'POST':
        return handle_appointment_submission(request)
    
    # GET request - formu göster
    try:
        clinics = Clinic.objects.all()
        doctors = Doctors.objects.all()
        
        # Debug bilgisi
        print(f"=== DEBUG BİLGİSİ ===")
        print(f"Bulunan poliklinik sayısı: {clinics.count()}")
        print(f"Bulunan doktor sayısı: {doctors.count()}")
        
        if clinics.count() == 0:
            print("⚠️ HİÇ POLİKLİNİK YOK! Önce poliklinik oluşturulmalı.")
        else:
            print("📋 POLİKLİNİKLER:")
            for clinic in clinics:
                print(f"  - {clinic.name} (ID: {clinic.id})")
        
        if doctors.count() == 0:
            print("⚠️ HİÇ DOKTOR YOK! Önce doktor oluşturulmalı.")
        else:
            print("👨‍⚕️ DOKTORLAR:")
            for doctor in doctors:
                clinic_info = doctor.clinic.name if doctor.clinic else "Klinik atanmamış"
                print(f"  - Dr. {doctor.name} {doctor.surname} - Klinik: {clinic_info}")
        
        print("=====================")
        
    except Exception as e:
        print(f"❌ HATA: {str(e)}")
        clinics = Clinic.objects.none()
        doctors = Doctors.objects.none()
    
    context = {
        'page_title': 'MEDORA - Randevu Al',
        'clinics': clinics,
        'doctors': doctors,
    }
    return render(request, 'take_appointments.html', context)

def handle_appointment_submission(request):
    """
    Randevu form gönderimini işler
    """
    try:
        # Hasta bilgilerini al
        patient_name = request.POST.get('patient_name')
        patient_surname = request.POST.get('patient_surname')
        patient_email = request.POST.get('patient_email')
        patient_phone = request.POST.get('patient_phone')
        patient_tc = request.POST.get('patient_tc')
        patient_birth = request.POST.get('patient_birth')
        
        # Randevu bilgilerini al
        clinic_id = request.POST.get('clinic')
        doctor_id = request.POST.get('doctor')
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        
        # Validasyon
        if not all([patient_name, patient_surname, patient_email, patient_phone, patient_tc, patient_birth, clinic_id, doctor_id, date_str, time_str]):
            messages.error(request, 'Lütfen tüm alanları doldurun.')
            return redirect('take_appointments')
        
        # Tarih ve saat kontrolü
        try:
            appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            appointment_time = datetime.strptime(time_str, '%H:%M').time()
        except ValueError:
            messages.error(request, 'Geçersiz tarih veya saat formatı.')
            return redirect('take_appointments')
        
        # Geçmiş tarih kontrolü
        if appointment_date < timezone.now().date():
            messages.error(request, 'Geçmiş tarih seçemezsiniz.')
            return redirect('take_appointments')
        
        # Pazar günü kontrolü
        if appointment_date.weekday() == 6:  # 0=Pazartesi, 6=Pazar
            messages.error(request, 'Pazar günleri randevu alınamaz.')
            return redirect('take_appointments')
        
        # Çalışma saatleri kontrolü (09:00-17:00)
        if appointment_time < datetime.strptime('09:00', '%H:%M').time() or \
           appointment_time > datetime.strptime('17:00', '%H:%M').time():
            messages.error(request, 'Çalışma saatleri dışında randevu alınamaz (09:00-17:00).')
            return redirect('take_appointments')
        
        # Doktor ve klinik kontrolü
        try:
            doctor = Doctors.objects.get(id=doctor_id)
            clinic = Clinic.objects.get(id=clinic_id)
        except (Doctors.DoesNotExist, Clinic.DoesNotExist):
            messages.error(request, 'Seçilen doktor veya klinik bulunamadı.')
            return redirect('take_appointments')
        
        # Randevu çakışması kontrolü
        existing_appointment = Appointment.objects.filter(
            doctor=doctor,
            date=appointment_date,
            time=appointment_time
        ).first()
        
        if existing_appointment:
            messages.error(request, f'Dr. {doctor.name} {doctor.surname} bu saatte ({time_str}) müsait değil. Lütfen başka bir saat seçin.')
            return redirect('take_appointments')
        
        try:
            birth_date = datetime.strptime(patient_birth, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Geçersiz doğum tarihi formatı.')
            return redirect('take_appointments')
        
        # Hasta oluştur veya güncelle
        patient, created = Patients.objects.get_or_create(
            email=patient_email,
            defaults={
                'name': patient_name,
                'surname': patient_surname,
                'phone': patient_phone,
                'tc_number': patient_tc,
                'date_of_birth': birth_date,
                'entry_date': timezone.now().date(),
                'image': None
            }
        )
        
        # Eğer hasta zaten varsa bilgilerini güncelle
        if not created:
            patient.name = patient_name
            patient.surname = patient_surname
            patient.phone = patient_phone
            patient.tc_number = patient_tc
            patient.date_of_birth = birth_date
            patient.save()
        
        # Randevu oluştur
        appointment = Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            date=appointment_date,
            time=appointment_time
        )
        
        messages.success(request, f'Randevunuz başarıyla oluşturuldu! Dr. {doctor.name} {doctor.surname} ile {appointment_date.strftime("%d.%m.%Y")} tarihinde saat {time_str} randevunuz var. Randevu No: {appointment.id}')
        return redirect('take_appointments')
        
    except Exception as e:
        messages.error(request, f'Randevu oluşturulurken bir hata oluştu: {str(e)}')
        return redirect('take_appointments')



@csrf_exempt
def get_doctors_by_clinic(request, clinic_id):
    """
    Klinik ID'sine göre doktorları döndürür (AJAX)
    """
    if request.method == 'GET':
        try:
            doctors = Doctors.objects.filter(clinic_id=clinic_id)
            doctors_data = []
            
            for doctor in doctors:
                doctors_data.append({
                    'id': doctor.id,
                    'name': doctor.name,
                    'surname': doctor.surname,
                    'email': doctor.email,
                    'phone': doctor.phone,
                    'image': doctor.image.url if doctor.image else None,
                    'clinic_name': doctor.clinic.name
                })
            
            return JsonResponse({'doctors': doctors_data})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def check_doctor_availability(request, doctor_id):
    """
    Doktorun belirli tarih ve saatte müsait olup olmadığını kontrol eder (AJAX)
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            date_str = data.get('date')
            time_str = data.get('time')
            
            if not date_str or not time_str:
                return JsonResponse({'error': 'Tarih ve saat gerekli'}, status=400)
            
            appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            appointment_time = datetime.strptime(time_str, '%H:%M').time()
            
            # Randevu çakışması kontrolü
            existing_appointment = Appointment.objects.filter(
                doctor_id=doctor_id,
                date=appointment_date,
                time=appointment_time
            ).exists()
            
            return JsonResponse({
                'available': not existing_appointment,
                'date': date_str,
                'time': time_str
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def get_available_time_slots(request, doctor_id, date):
    """
    Doktorun belirli tarihte müsait saatlerini döndürür (AJAX)
    """
    if request.method == 'GET':
        try:
            appointment_date = datetime.strptime(date, '%Y-%m-%d').date()
            
            # Tüm çalışma saatleri
            all_time_slots = [
                '09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
                '14:00', '14:30', '15:00', '15:30', '16:00', '16:30'
            ]
            
            # Dolu saatleri al
            booked_times = Appointment.objects.filter(
                doctor_id=doctor_id,
                date=appointment_date
            ).values_list('time', flat=True)
            
            # Dolu saatleri string formatına çevir
            booked_time_strings = [time.strftime('%H:%M') for time in booked_times]
            
            # Müsait saatleri hesapla
            available_slots = [slot for slot in all_time_slots if slot not in booked_time_strings]
            
            return JsonResponse({
                'available_slots': available_slots,
                'booked_slots': booked_time_strings,
                'date': date
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)
