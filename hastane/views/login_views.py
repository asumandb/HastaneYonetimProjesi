from django.shortcuts import render

def login_select_view(request):
    return render(request, 'loginpage/login_select.html')

def admin_login_view(request):
    return render(request, 'loginpage/admin_login.html')

def doctor_login_view(request):
    return render(request, 'loginpage/doctor_login.html')

def patient_login_view(request):
    return render(request, 'loginpage/patient_login.html')
