from django.shortcuts import render, redirect
from django.contrib import messages
from ..models.doctors_model import Doctors
from ..models.clinic_model import Clinic
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

def doctor_create(request):
    if request.method == 'POST':
        try:
            # POST verilerini al
            name = request.POST.get('name')
            surname = request.POST.get('surname')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            clinic_id = request.POST.get('clinic')
            speciality = request.POST.get('speciality')
            image = request.FILES.get('image')
            
            # Yeni doktor oluştur
            doctor = Doctors.objects.create(
                name=name,
                surname=surname,
                email=email,
                phone=phone,
                clinic_id=clinic_id,
                speciality=speciality,
                image=image
            )
            
            messages.success(request, f'Doktor {doctor.name} {doctor.surname} başarıyla eklendi.')
            return redirect('doctor_list')
            
        except Exception as e:
            messages.error(request, f'Doktor eklenirken hata oluştu: {str(e)}')
    
    # GET isteği için clinic listesini al
    clinics = Clinic.objects.all()
    
    return render(request, 'hastane/doctor_form.html', {
        'title': 'Yeni Doktor Ekle',
        'clinics': clinics
    })

def doctor_list(request):
    doctors = Doctors.objects.all()
    return render(request, 'doctors.html', {'doctors': doctors, 'title': 'Doktorlar'})

def get_clinics(request):
    clinics = Clinic.objects.all().values('id', 'name')
    return JsonResponse(list(clinics), safe=False)

@csrf_exempt
def doctor_delete(request, doctor_id):
    if request.method == 'POST':
        try:
            doctor = Doctors.objects.get(id=doctor_id)
            doctor.delete()
            return JsonResponse({'success': True})
        except Doctors.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Doktor bulunamadı.'}, status=404)
    return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def doctor_update(request, doctor_id):
    try:
        doctor = Doctors.objects.get(id=doctor_id)
    except Doctors.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Doktor bulunamadı.'}, status=404)
    if request.method == 'GET':
        # Doktor bilgilerini JSON olarak döndür
        return JsonResponse({
            'id': doctor.id,
            'name': doctor.name,
            'surname': doctor.surname,
            'email': doctor.email,
            'phone': doctor.phone,
            'clinic': doctor.clinic_id,
            'image': doctor.image.url if doctor.image else ''
        })
    elif request.method == 'POST':
        doctor.name = request.POST.get('name', doctor.name)
        doctor.surname = request.POST.get('surname', doctor.surname)
        doctor.email = request.POST.get('email', doctor.email)
        doctor.phone = request.POST.get('phone', doctor.phone)
        doctor.clinic_id = request.POST.get('clinic', doctor.clinic_id)
        if request.FILES.get('image'):
            doctor.image = request.FILES['image']
        doctor.save()
        return JsonResponse({'success': True})
    return HttpResponseNotAllowed(['GET', 'POST'])
