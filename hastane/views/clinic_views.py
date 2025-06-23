from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from ..models.clinic_model import Clinic
from ..models.doctors_model import Doctors

# CREATE - Poliklinik oluşturma
def clinic_create(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            address = request.POST.get('address')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            website = request.POST.get('website')
            image = request.FILES.get('image')
            
            clinic = Clinic.objects.create(
                name=name,
                address=address,
                phone=phone,
                email=email,
                website=website,
                image=image
            )
            
            messages.success(request, f'Poliklinik {clinic.name} başarıyla oluşturuldu.')
            return redirect('clinic_list')
            
        except Exception as e:
            messages.error(request, f'Poliklinik oluşturulurken hata oluştu: {str(e)}')
    
    return render(request, 'clinic_form.html', {
        'title': 'Yeni Poliklinik Oluştur'
    })

# READ - Poliklinik listesi
def clinic_list(request):
    clinics = Clinic.objects.all()
    return render(request, 'polyclinics.html', {
        'clinics': clinics,
        'title': 'Poliklinikler'
    })

# READ - Poliklinik detayı (doktorları ile birlikte)
def clinic_detail(request, clinic_id):
    clinic = get_object_or_404(Clinic, id=clinic_id)
    doctors = Doctors.objects.filter(clinic=clinic)
    
    return render(request, 'clinic_detail.html', {
        'clinic': clinic,
        'doctors': doctors,
        'title': f'{clinic.name} Detayları'
    })

# UPDATE - Poliklinik güncelleme
def clinic_update(request, clinic_id):
    clinic = get_object_or_404(Clinic, id=clinic_id)
    
    if request.method == 'POST':
        try:
            clinic.name = request.POST.get('name')
            clinic.address = request.POST.get('address')
            clinic.phone = request.POST.get('phone')
            clinic.email = request.POST.get('email')
            clinic.website = request.POST.get('website')
            
            if 'image' in request.FILES:
                clinic.image = request.FILES['image']
            
            clinic.save()
            
            messages.success(request, f'Poliklinik {clinic.name} başarıyla güncellendi.')
            return redirect('clinic_detail', clinic_id=clinic.id)
            
        except Exception as e:
            messages.error(request, f'Poliklinik güncellenirken hata oluştu: {str(e)}')
    
    return render(request, 'clinic_form.html', {
        'clinic': clinic,
        'title': f'{clinic.name} Güncelle'
    })

# DELETE - Poliklinik silme
def clinic_delete(request, clinic_id):
    clinic = get_object_or_404(Clinic, id=clinic_id)
    
    if request.method == 'POST':
        try:
            clinic_name = clinic.name
            clinic.delete()
            messages.success(request, f'Poliklinik {clinic_name} başarıyla silindi.')
            return redirect('clinic_list')
            
        except Exception as e:
            messages.error(request, f'Poliklinik silinirken hata oluştu: {str(e)}')
    
    return render(request, 'clinic_confirm_delete.html', {
        'clinic': clinic,
        'title': f'{clinic.name} Sil'
    })

# Modal için doktor listesi (AJAX)
def get_available_doctors(request, clinic_id):
    clinic = get_object_or_404(Clinic, id=clinic_id)
    
    # Atanmamış doktorları al
    unassigned_doctors = Doctors.objects.filter(clinic__isnull=True)
    assigned_doctors = Doctors.objects.filter(clinic=clinic)
    
    # JSON response için doktor verilerini hazırla
    unassigned_data = []
    for doctor in unassigned_doctors:
        unassigned_data.append({
            'id': doctor.id,
            'name': f"{doctor.name} {doctor.surname}",
            'speciality': doctor.speciality,
            'email': doctor.email
        })
    
    assigned_data = []
    for doctor in assigned_doctors:
        assigned_data.append({
            'id': doctor.id,
            'name': f"{doctor.name} {doctor.surname}",
            'speciality': doctor.speciality,
            'email': doctor.email
        })
    
    return JsonResponse({
        'unassigned_doctors': unassigned_data,
        'assigned_doctors': assigned_data,
        'clinic_name': clinic.name
    })

# Modal ile doktor atama (AJAX)
def assign_doctors_modal(request, clinic_id):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        clinic = get_object_or_404(Clinic, id=clinic_id)
        
        try:
            doctor_ids = request.POST.getlist('doctor_ids[]')
            
            if doctor_ids:
                # Seçilen doktorları bu polikliğe ata
                Doctors.objects.filter(id__in=doctor_ids).update(clinic=clinic)
                
                return JsonResponse({
                    'success': True,
                    'message': f'{len(doctor_ids)} doktor {clinic.name} polikliğine atandı.',
                    'assigned_count': len(doctor_ids)
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Lütfen en az bir doktor seçin.'
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Doktor atama işlemi başarısız: {str(e)}'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Geçersiz istek.'
    })

# Doktor atama fonksiyonu (eski versiyon - modal için güncellendi)
def assign_doctors_to_clinic(request, clinic_id):
    clinic = get_object_or_404(Clinic, id=clinic_id)
    
    if request.method == 'POST':
        doctor_ids = request.POST.getlist('doctors')
        
        try:
            # Seçilen doktorları bu poliklinikle ilişkilendir
            Doctors.objects.filter(id__in=doctor_ids).update(clinic=clinic)
            
            messages.success(request, f'{len(doctor_ids)} doktor {clinic.name} polikliğine atandı.')
            return redirect('clinic_detail', clinic_id=clinic.id)
            
        except Exception as e:
            messages.error(request, f'Doktor atama işlemi başarısız: {str(e)}')
    
    # Atanmamış doktorları al
    unassigned_doctors = Doctors.objects.filter(clinic__isnull=True)
    assigned_doctors = Doctors.objects.filter(clinic=clinic)
    
    return render(request, 'hastane/assign_doctors.html', {
        'clinic': clinic,
        'unassigned_doctors': unassigned_doctors,
        'assigned_doctors': assigned_doctors,
        'title': f'{clinic.name} - Doktor Atama'
    })
