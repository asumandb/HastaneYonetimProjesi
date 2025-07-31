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
from django.urls import path, include
from hastane.views.patient_registration_views import patient_registration_view, patient_list, patient_update
from hastane.views.clinic_views import clinic_create, clinic_list, clinic_update, clinic_delete, clinic_detail, get_available_doctors, assign_doctors_modal, assign_doctors_to_clinic
from hastane.views.doctor_views import doctor_create, doctor_list, doctor_update, doctor_delete
from hastane.views.appointment_views import appointment_calendar, day_appointments, check_doctor_availability, get_doctor_available_slots, delete_appointment, doctor_appointments, appointment_create, appointment_list_json, appointment_table_partial
from hastane.views.prescriptions_views import prescriptions_view
from hastane.views.rooms_views import room_list, add_room, update_room, delete_room, room_dropdown, room_description

from hastane.views.login_views import login_select_view, admin_login_view, doctor_login_view
from hastane.views.index_views import index_view
from hastane.views.take_appointment_views import take_appointments_view
from hastane.views.take_appointment_views import get_doctors_by_clinic, check_doctor_availability

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hasta-kayit/', patient_registration_view, name='patient_registration'),
    path('patients/', patient_list, name='patient_list'),
    path('patients/<int:patient_id>/update/', patient_update, name='patient_update'),

    path('poliklinikler/', clinic_list, name='polyclinics'),
    path('poliklinik/olustur/', clinic_create, name='clinic_create'),
    path('poliklinik/<int:clinic_id>/', clinic_detail, name='clinic_detail'),
    path('poliklinik/<int:clinic_id>/guncelle/', clinic_update, name='clinic_update'),
    path('poliklinik/<int:clinic_id>/sil/', clinic_delete, name='clinic_delete'),
    path('poliklinik/<int:clinic_id>/doktorlar/', get_available_doctors, name='get_available_doctors'),
    path('poliklinik/<int:clinic_id>/doktor-atama/', assign_doctors_modal, name='assign_doctors_modal'),
    path('poliklinik/<int:clinic_id>/doktor-atama-form/', assign_doctors_to_clinic, name='assign_doctors_to_clinic'),

    path('doktor/olustur/', doctor_create, name='doctor_create'),
    path('doktor/guncelle/<int:doctor_id>/', doctor_update, name='doctor_update'),
    path('doktor/sil/<int:doctor_id>/', doctor_delete, name='doctor_delete'),
    path('doktorlar/', doctor_list, name='doctor_list'),

    path('randevular/', appointment_calendar, name='appointments'),
    path('randevu/ekle/', appointment_create, name='appointment_create'),
    path('randevu/takvim/', appointment_calendar, name='appointment_calendar'),
    path('randevu/gun/<int:year>/<int:month>/<int:day>/', day_appointments, name='day_appointments'),
    path('randevu/doktor-uygunluk/<int:doctor_id>/', check_doctor_availability, name='doctor_availability_check'),
    path('randevu/doktor-saatler/<int:doctor_id>/', get_doctor_available_slots, name='get_doctor_available_slots'),
    path('randevu/sil/<int:appointment_id>/', delete_appointment, name='delete_appointment'),
    path('randevu/doktor/<int:doctor_id>/', doctor_appointments, name='doctor_appointments'),
    path('randevular/data/', appointment_list_json, name='appointment_list_json'),
    path('randevu/tablo/', appointment_table_partial, name='appointment_table_partial'),

    path('receteler/', prescriptions_view, name='prescriptions'),

    path('odalar/', room_list, name='room_list'),
    path('oda/ekle/', add_room, name='add_room'),
    path('oda/guncelle/<int:room_id>/', update_room, name='oda_guncelle'),
    path('oda/sil/<int:room_id>/', delete_room, name='oda_sil'),
    path('oda/dropdown/', room_dropdown, name='room_dropdown'),
    path('oda/aciklama/<int:room_id>/', room_description, name='oda_aciklama'),

    path('login/', login_select_view, name='login_select'),
    path('login/admin/', admin_login_view, name='admin_login'),
    path('login/doctor/', doctor_login_view, name='doctor_login'),


    path('randevu-al/', take_appointments_view, name='take_appointments'),

    path('api/clinics/<int:clinic_id>/doctors/', get_doctors_by_clinic, name='get_doctors_by_clinic'),
    path('api/doctors/<int:doctor_id>/availability/', check_doctor_availability, name='check_doctor_availability'),

    path('', index_view, name='index'),

    path('', include('hastane.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)