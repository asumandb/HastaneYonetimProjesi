from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from hastane.models import Patients
from hastane.models.doctors_model import Doctors
from django.contrib.auth.hashers import check_password

def login_select_view(request):
    return render(request, 'loginPage/login_select.html')

def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Admin kullanıcısını doğrula
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, 'Admin girişi başarılı!')
            return redirect('patient_registration')  # Hasta kayıt sayfasına yönlendir
        else:
            messages.error(request, 'Geçersiz kullanıcı adı veya şifre!')
    
    return render(request, 'loginPage/admin_login.html')

def doctor_login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')  # Email olarak kullanıcı adı alınıyor
        password = request.POST.get('password')
        
        try:
            # Email ile doktoru bul
            doctor = Doctors.objects.get(email=email)
            
            # Şifreyi kontrol et
            password_check_result = check_password(password, doctor.password)
            
            if doctor.password and password_check_result:
                # Session'a doktor bilgisini kaydet
                request.session['doctor_id'] = doctor.id
                request.session['doctor_name'] = f"{doctor.name} {doctor.surname}"
                messages.success(request, f'Hoş geldiniz, Dr. {doctor.name} {doctor.surname}!')
                return redirect('doctor_dashboard')  # Doktor dashboard'una yönlendir
            else:
                messages.error(request, 'Geçersiz email veya şifre!')
        except Doctors.DoesNotExist:
            messages.error(request, 'Bu email ile kayıtlı doktor bulunamadı!')
    
    return render(request, 'loginPage/doctor_login.html')

def doctor_dashboard_view(request):
    # Doktor girişi kontrolü
    if 'doctor_id' not in request.session:
        messages.error(request, 'Lütfen önce giriş yapın!')
        return redirect('doctor_login')
    
    doctor_id = request.session['doctor_id']
    doctor_name = request.session['doctor_name']
    
    context = {
        'doctor_name': doctor_name,
        'doctor_id': doctor_id
    }
    
    return render(request, 'doctor_dashboard.html', context)

def doctor_logout_view(request):
    # Session'ı temizle
    if 'doctor_id' in request.session:
        del request.session['doctor_id']
    if 'doctor_name' in request.session:
        del request.session['doctor_name']
    
    messages.success(request, 'Başarıyla çıkış yaptınız!')
    return redirect('login_select')


