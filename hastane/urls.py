from django.urls import path
from .views.polyclinic_api import polyclinic_api
from .views.doctor_views import get_clinics

urlpatterns = [
    path('api/polyclinics/', polyclinic_api, name='polyclinic_api'),
    path('api/clinics/', get_clinics, name='get_clinics'),
] 