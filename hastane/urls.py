from django.urls import path
from .views.polyclinic_api import polyclinic_api

urlpatterns = [
    path('api/polyclinics/', polyclinic_api, name='polyclinic_api'),
] 