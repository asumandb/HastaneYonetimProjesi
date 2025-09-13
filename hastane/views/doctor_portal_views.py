from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from hastane.models.appointments_model import Appointment
from hastane.models.patients_model import Patients
from hastane.models.prescriptions_model import Prescriptions


def _require_doctor_session(request):
	if 'doctor_id' not in request.session:
		messages.error(request, 'Lütfen önce giriş yapın!')
		return None
	return {
		'doctor_id': request.session['doctor_id'],
		'doctor_name': request.session.get('doctor_name', ''),
	}


def doctor_my_appointments_view(request):
	session_info = _require_doctor_session(request)
	if session_info is None:
		return redirect('doctor_login')
	appointments = Appointment.objects.filter(doctor_id=session_info['doctor_id']).order_by('-date', '-time')
	return render(request, 'doctor/appointments.html', {
		'appointments': appointments,
		'doctor_name': session_info['doctor_name'],
	})


def doctor_my_patients_view(request):
	session_info = _require_doctor_session(request)
	if session_info is None:
		return redirect('doctor_login')
	patients = Patients.objects.filter(randevular__doctor_id=session_info['doctor_id']).distinct().order_by('name', 'surname')
	return render(request, 'doctor/patients.html', {
		'patients': patients,
		'doctor_name': session_info['doctor_name'],
	})


def doctor_my_prescriptions_view(request):
	session_info = _require_doctor_session(request)
	if session_info is None:
		return redirect('doctor_login')
	prescriptions = Prescriptions.objects.select_related('appointment', 'appointment__patient').filter(
		appointment__doctor_id=session_info['doctor_id']
	).order_by('-id')
	return render(request, 'doctor/prescriptions.html', {
		'prescriptions': prescriptions,
		'doctor_name': session_info['doctor_name'],
	})


@require_http_methods(["GET", "POST"])
def doctor_prescription_create_view(request):
	session_info = _require_doctor_session(request)
	if session_info is None:
		return redirect('doctor_login')

	if request.method == 'POST':
		appointment_id = request.POST.get('appointment_id')
		medicine = request.POST.get('medicine', '').strip()
		if not appointment_id or not medicine:
			messages.error(request, 'Lütfen randevu ve ilaç bilgisini doldurun.')
			return redirect('doctor_prescription_create')
		appointment = get_object_or_404(Appointment, id=appointment_id, doctor_id=session_info['doctor_id'])
		Prescriptions.objects.create(appointment=appointment, medicine=medicine)
		messages.success(request, 'Reçete başarıyla oluşturuldu.')
		return redirect('doctor_my_prescriptions')

	# GET
	appointments = Appointment.objects.filter(doctor_id=session_info['doctor_id']).order_by('-date', '-time')
	return render(request, 'doctor/prescription_form.html', {
		'appointments': appointments,
		'doctor_name': session_info['doctor_name'],
	})


def doctor_prescription_edit_view(request, prescription_id):
	session_info = _require_doctor_session(request)
	if session_info is None:
		return redirect('doctor_login')

	prescription = get_object_or_404(
		Prescriptions.objects.select_related('appointment', 'appointment__patient'),
		id=prescription_id,
		appointment__doctor_id=session_info['doctor_id'],
	)

	if request.method == 'POST':
		medicine = request.POST.get('medicine', '').strip()
		if not medicine:
			messages.error(request, 'İlaç bilgisini boş bırakmayın.')
			return redirect('doctor_prescription_edit', prescription_id=prescription.id)
		prescription.medicine = medicine
		prescription.save()
		messages.success(request, 'Reçete güncellendi.')
		return redirect('doctor_my_prescriptions')

	return render(request, 'doctor/prescription_edit.html', {
		'prescription': prescription,
		'doctor_name': session_info['doctor_name'],
	})

