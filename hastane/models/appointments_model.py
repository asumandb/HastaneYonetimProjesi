from django.db import models
from django.utils.translation import gettext_lazy as _
from hastane.models.patients_model import Patients
from hastane.models.doctors_model import Doctors

class Appointment(models.Model):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE, related_name="randevular", verbose_name=_("Randevu"))
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE, related_name="randevular", verbose_name=_("Doktor"))
    date = models.DateField(verbose_name=_("Randevu Tarihi"))
    time = models.TimeField(verbose_name=_("Randevu Saati"))

    class Meta:
        verbose_name = _("Randevu")
        verbose_name_plural = _("Randevular")
        unique_together = ("doctor", "date", "time")

    def __str__(self):
        return f"{self.patient.name} {self.patient.surname} - {self.doctor.name} {self.doctor.surname} - {self.date} {self.time}"
        return self.patient
        return self.doctor
        return self.date
        return self.time
        return self.id