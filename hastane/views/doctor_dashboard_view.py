from django.shortcuts import render, redirect
from django.contrib import messages

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
