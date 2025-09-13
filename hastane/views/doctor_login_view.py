from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from hastane.models.doctors_model import Doctors

def doctor_login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        try:
            doctor = Doctors.objects.get(email=email)
            if check_password(password, doctor.password):
                # Giriş başarılı, session oluştur
                request.session['doctor_id'] = doctor.id
                request.session['doctor_name'] = f"{doctor.name} {doctor.surname}"
                messages.success(request, f'Hoş geldiniz, Dr. {doctor.name} {doctor.surname}!')
                return redirect('doctor_dashboard')  # dashboard sayfasına yönlendir
            else:
                messages.error(request, 'Şifre yanlış!')
        except Doctors.DoesNotExist:
            messages.error(request, 'Bu email ile kayıtlı doktor bulunamadı!')

    # GET isteğinde ya da hata durumunda login sayfasını göster
    return render(request, 'loginPage/doctor_login.html')
