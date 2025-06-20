from django.shortcuts import render, redirect
from django.contrib import messages
from ..models.doctors_model import Doctors
from ..models.clinic_model import Clinic

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
