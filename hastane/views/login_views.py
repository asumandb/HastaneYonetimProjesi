from django.shortcuts import render, redirect
from django.contrib import messages
from hastane.models import Patients

def login_select_view(request):
    return render(request, 'loginpage/login_select.html')

def admin_login_view(request):
    return render(request, 'loginpage/admin_login.html')

def doctor_login_view(request):
    return render(request, 'loginpage/doctor_login.html')

def patient_login_view(request):
    return render(request, 'loginpage/patient_login.html')

def patient_register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        # Basit şifre kontrolü
        if password1 != password2:
            messages.error(request, 'Şifreler eşleşmiyor!')
            return render(request, 'loginpage/patient_register.html')
        # Kullanıcı adı veya e-posta daha önce alınmış mı kontrolü
        if Patients.objects.filter(email=email).exists():
            messages.error(request, 'Bu e-posta ile kayıtlı bir kullanıcı zaten var!')
            return render(request, 'loginpage/patient_register.html')
        # Kayıt
        Patients.objects.create(
            name=first_name,
            surname=last_name,
            email=email,
            phone='',
            image=None,
            tc_number='',
            date_of_birth=None,
            entry_date=None,
            exit_date=None
        )
        messages.success(request, 'Kayıt başarılı! Giriş yapabilirsiniz.')
        return redirect('patient_login')
    return render(request, 'loginpage/patient_register.html')
