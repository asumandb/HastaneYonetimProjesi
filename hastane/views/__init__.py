from .doctor_views import doctor_create
from .clinic_views import clinic_create, clinic_list, clinic_detail, clinic_update, clinic_delete, get_available_doctors, assign_doctors_modal, assign_doctors_to_clinic
from .appointment_views import appointment_calendar, day_appointments, check_doctor_availability, get_doctor_available_slots, delete_appointment, doctor_appointments
from .patient_registration_views import patient_registration_view
from .rooms_views import room_list, add_room, update_room, delete_room, room_dropdown, room_description
