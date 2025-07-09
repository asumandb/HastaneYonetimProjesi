from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta, date
from ..models.appointments_model import Appointment
from ..models.doctors_model import Doctors
from ..models.patients_model import Patients
from django.template.loader import render_to_string

# Randevu takvimi görüntüleme
def appointment_calendar(request):
    # Tarih parametrelerini al
    year = request.GET.get('year', timezone.now().year)
    month = request.GET.get('month', timezone.now().month)
    
    try:
        year = int(year)
        month = int(month)
        current_date = date(year, month, 1)
    except ValueError:
        current_date = timezone.now().date()
    
    # Ayın ilk ve son günü
    first_day = current_date.replace(day=1)
    last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    # Takvim için günleri hazırla
    calendar_days = []
    start_date = first_day - timedelta(days=first_day.weekday())
    
    for i in range(42):  # 6 hafta x 7 gün
        day_date = start_date + timedelta(days=i)
        
        # O günkü randevuları al
        day_appointments = Appointment.objects.filter(date=day_date)
        
        calendar_days.append({
            'date': day_date,
            'appointments': day_appointments,
            'appointment_count': day_appointments.count(),
            'is_current_month': day_date.month == current_date.month,
            'is_today': day_date == timezone.now().date()
        })
    
    # Doktorları al (filtreleme için)
    doctors = Doctors.objects.all()
    patients = Patients.objects.all()
    appointments = Appointment.objects.all().order_by('-date', '-time')
    return render(request, 'appointments.html', {
        'calendar_days': calendar_days,
        'current_date': current_date,
        'doctors': doctors,
        'patients': patients,
        'appointments': appointments,
        'title': 'Randevu Takvimi'
    })

# Belirli bir günün randevularını görüntüleme
def day_appointments(request, year, month, day):
    try:
        appointment_date = date(int(year), int(month), int(day))
    except ValueError:
        messages.error(request, 'Geçersiz tarih.')
        return redirect('appointment_calendar')
    
    # O günkü randevuları al
    appointments = Appointment.objects.filter(date=appointment_date).order_by('time')
    
    # Saat dilimlerine göre grupla
    time_slots = {}
    for hour in range(8, 18):  # 08:00-18:00 arası
        time_slots[f'{hour:02d}:00'] = []
        time_slots[f'{hour:02d}:30'] = []
    
    for appointment in appointments:
        time_str = appointment.time.strftime('%H:%M')
        if time_str in time_slots:
            time_slots[time_str].append(appointment)
    
    # Doktorları al (filtreleme için)
    doctors = Doctors.objects.all()
    patients = Patients.objects.all()
    
    return render(request, 'appointments.html', {
        'appointment_date': appointment_date,
        'time_slots': time_slots,
        'appointments': appointments,
        'title': f'{appointment_date.strftime("%d %B %Y")} Randevuları'
    })

# Doktor uygunluk kontrolü
def check_doctor_availability(request, doctor_id):
    doctor = get_object_or_404(Doctors, id=doctor_id)
    
    if request.method == 'POST' or request.method == 'GET':
        check_date = request.POST.get('date') or request.GET.get('date')
        check_time = request.POST.get('time') or request.GET.get('time')
        appointment_id = request.POST.get('appointment_id') or request.GET.get('appointment_id')
        try:
            # Tarih ve saat formatını kontrol et
            appointment_date = datetime.strptime(check_date, '%Y-%m-%d').date()
            appointment_time = datetime.strptime(check_time, '%H:%M').time()
            # Bu doktorun o tarih ve saatte randevusu var mı?
            existing_appointment = Appointment.objects.filter(
                doctor=doctor,
                date=appointment_date,
                time=appointment_time
            )
            if appointment_id:
                existing_appointment = existing_appointment.exclude(id=appointment_id)
            existing_appointment = existing_appointment.first()
            if existing_appointment:
                return JsonResponse({
                    'available': False,
                    'message': f'Bu saatte {existing_appointment.patient.name} {existing_appointment.patient.surname} ile randevu var.',
                    'existing_patient': f'{existing_appointment.patient.name} {existing_appointment.patient.surname}'
                })
            else:
                return JsonResponse({
                    'available': True,
                    'message': 'Bu saat müsait.',
                    'doctor_name': f'{doctor.name} {doctor.surname}',
                    'speciality': doctor.speciality
                })
        except ValueError:
            return JsonResponse({
                'available': False,
                'message': 'Geçersiz tarih veya saat formatı.'
            })
    return JsonResponse({
        'available': False,
        'message': 'Geçersiz istek.'
    })

# Doktorun müsait saatlerini getir
def get_doctor_available_slots(request, doctor_id):
    doctor = get_object_or_404(Doctors, id=doctor_id)
    
    if request.method == 'GET':
        check_date = request.GET.get('date')
        
        try:
            appointment_date = datetime.strptime(check_date, '%Y-%m-%d').date()
            
            # O günkü mevcut randevuları al
            existing_appointments = Appointment.objects.filter(
                doctor=doctor,
                date=appointment_date
            ).values_list('time', flat=True)
            
            # Müsait saatleri hesapla (08:00-18:00, 30 dakikalık aralıklarla)
            available_slots = []
            busy_slots = []
            
            for hour in range(8, 18):
                for minute in [0, 30]:
                    time_slot = f'{hour:02d}:{minute:02d}'
                    time_obj = datetime.strptime(time_slot, '%H:%M').time()
                    
                    if time_obj in existing_appointments:
                        busy_slots.append(time_slot)
                    else:
                        available_slots.append(time_slot)
            
            return JsonResponse({
                'available_slots': available_slots,
                'busy_slots': busy_slots,
                'doctor_name': f'{doctor.name} {doctor.surname}',
                'date': check_date
            })
            
        except ValueError:
            return JsonResponse({
                'error': 'Geçersiz tarih formatı.'
            })
    
    return JsonResponse({
        'error': 'Geçersiz istek.'
    })

# Randevu oluşturma (uygunluk kontrolü ile)
def appointment_create(request):
    if request.method == 'POST':
        try:
            appointment_id = request.POST.get('appointment_id')
            patient_id = request.POST.get('patient')
            doctor_id = request.POST.get('doctor')
            appointment_date = request.POST.get('date')
            appointment_time = request.POST.get('time')

            if appointment_id:
                # Güncelleme
                appointment = Appointment.objects.get(id=appointment_id)
                # Uygunluk kontrolü (güncellenen randevu hariç)
                existing_appointment = Appointment.objects.filter(
                    doctor_id=doctor_id,
                    date=appointment_date,
                    time=appointment_time
                ).exclude(id=appointment_id).first()
                if existing_appointment:
                    return JsonResponse({'success': False, 'error': 'Bu saatte doktorun başka bir randevusu var.'})
                appointment.patient_id = patient_id
                appointment.doctor_id = doctor_id
                appointment.date = appointment_date
                appointment.time = appointment_time
                appointment.save()
                return JsonResponse({'success': True})
            else:
                # Ekleme
                existing_appointment = Appointment.objects.filter(
                    doctor_id=doctor_id,
                    date=appointment_date,
                    time=appointment_time
                ).first()
                if existing_appointment:
                    return JsonResponse({'success': False, 'error': 'Bu saatte doktorun başka bir randevusu var.'})
                appointment = Appointment.objects.create(
                    patient_id=patient_id,
                    doctor_id=doctor_id,
                    date=appointment_date,
                    time=appointment_time
                )
                return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Randevu oluşturulurken/güncellenirken hata oluştu: {str(e)}'})

    # GET isteği için gerekli verileri al
    appointment_id = request.GET.get('appointment_id')
    if appointment_id:
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            return JsonResponse({
                'id': appointment.id,
                'patient': appointment.patient_id,
                'doctor': appointment.doctor_id,
                'date': str(appointment.date),
                'time': str(appointment.time),
                'title': 'Randevu Düzenle'
            })
        except Appointment.DoesNotExist:
            return JsonResponse({'error': 'Randevu bulunamadı.'}, status=404)
    # Yeni randevu için boş değerler
    return JsonResponse({
        'id': '',
        'patient': '',
        'doctor': '',
        'date': '',
        'time': '',
        'title': 'Yeni Randevu Ekle'
    })

# Randevu silme
def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        try:
            appointment.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Geçersiz istek.'})

# Doktor randevularını listele
def doctor_appointments(request, doctor_id):
    doctor = get_object_or_404(Doctors, id=doctor_id)
    
    # Tarih filtresi
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    appointments = Appointment.objects.filter(doctor=doctor)
    
    if start_date:
        appointments = appointments.filter(date__gte=start_date)
    if end_date:
        appointments = appointments.filter(date__lte=end_date)
    
    appointments = appointments.order_by('date', 'time')
    
    return render(request, 'appointments.html', {
        'doctor': doctor,
        'appointments': appointments,
        'title': f'{doctor.name} {doctor.surname} - Randevular',
        'patients': Patients.objects.all(),
        'doctors': Doctors.objects.all(),
    })

def appointment_list_json(request):
    appointments = Appointment.objects.all()
    events = []
    for appointment in appointments:
        events.append({
            "id": appointment.id,
            "title": f"{appointment.patient.name} {appointment.patient.surname} - {appointment.doctor.name} {appointment.doctor.surname}",
            "start": f"{appointment.date}T{appointment.time.strftime('%H:%M:%S')}",
            "end": f"{appointment.date}T{appointment.time.strftime('%H:%M:%S')}",
        })
    return JsonResponse(events, safe=False)

def appointment_table_partial(request):
    appointments = Appointment.objects.all().order_by('-date', '-time')
    return render(request, 'appointments.html', {
        'appointments': appointments,
        'patients': Patients.objects.all(),
        'doctors': Doctors.objects.all(),
    })
