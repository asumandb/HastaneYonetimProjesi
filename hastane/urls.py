from django.urls import path
from .views.polyclinic_api import polyclinic_api
from .views.doctor_views import get_clinics
from .views.prescriptions_views import (
    prescriptions_view,
    api_prescriptions,
    api_appointments,
    api_add_prescription
)

urlpatterns = [
    path('api/polyclinics/', polyclinic_api, name='polyclinic_api'),
    path('api/clinics/', get_clinics, name='get_clinics'),
    path('prescriptions/', prescriptions_view, name='prescriptions'),
    path('api/prescriptions/', api_prescriptions, name='api_prescriptions'),
    path('api/appointments/', api_appointments, name='api_appointments'),
    path('api/prescriptions/add/', api_add_prescription, name='api_add_prescription'),
]