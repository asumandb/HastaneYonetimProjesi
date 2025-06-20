"""hastane_yonetim URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from hastane.views.patient_registration_views import patient_registration_view, patient_list
from hastane.views.clinic_views import clinic_create, clinic_list, clinic_update, clinic_delete, clinic_detail, get_available_doctors, assign_doctors_modal, assign_doctors_to_clinic
from hastane.views.doctor_views import doctor_create
from hastane.views.appointment_views import appointment_calendar, day_appointments, check_doctor_availability, get_doctor_available_slots, delete_appointment, doctor_appointments
from hastane.views.prescriptions_views import prescriptions_view
from hastane.views.beds_views import beds_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hasta-kayit/', patient_registration_view, name='patient_registration'),
    path('patients/', patient_list, name='patient_list'),
    path('poliklinikler/', clinic_list, name='polyclinics'),
    path('poliklinik/olustur/', clinic_create, name='clinic_create'),
    path('poliklinik/<int:clinic_id>/', clinic_detail, name='clinic_detail'),
    path('poliklinik/<int:clinic_id>/guncelle/', clinic_update, name='clinic_update'),
    path('poliklinik/<int:clinic_id>/sil/', clinic_delete, name='clinic_delete'),
    path('poliklinik/<int:clinic_id>/doktorlar/', get_available_doctors, name='get_available_doctors'),
    path('poliklinik/<int:clinic_id>/doktor-atama/', assign_doctors_modal, name='assign_doctors_modal'),
    path('poliklinik/<int:clinic_id>/doktor-atama-form/', assign_doctors_to_clinic, name='assign_doctors_to_clinic'),
    path('doktor/olustur/', doctor_create, name='doctor_create'),
     path('randevular/', appointment_calendar, name='appointments'),
    path('randevu/takvim/', appointment_calendar, name='appointment_calendar'),
    path('randevu/gun/<int:year>/<int:month>/<int:day>/', day_appointments, name='day_appointments'),
    path('randevu/doktor-uygunluk/<int:doctor_id>/', check_doctor_availability, name='check_doctor_availability'),
    path('randevu/doktor-saatler/<int:doctor_id>/', get_doctor_available_slots, name='get_doctor_available_slots'),
    path('randevu/sil/<int:appointment_id>/', delete_appointment, name='delete_appointment'),
    path('randevu/doktor/<int:doctor_id>/', doctor_appointments, name='doctor_appointments'),
    path('receteler/', prescriptions_view, name='prescriptions'),
    path('yataklar/', beds_view, name='beds'),
]

