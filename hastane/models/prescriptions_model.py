from django.db import models
from django.utils.translation import gettext_lazy as _
from .appointments_model import Appointment

class Prescriptions(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name="recete", verbose_name=_("Randevu"))
    medicine = models.TextField(_("İlaçlar"),  help_text="İlaç isimlerini ve kullanım detaylarını giriniz.")
    
    class Meta:
        verbose_name = _("Reçete")
        verbose_name_plural = _("Reçeteler")

    def __str__(self):
        return f"{self.appointment.patient.name} {self.appointment.patient.surname} - {self.appointment.doctor.name} {self.appointment.doctor.surname} - {self.appointment.date} {self.appointment.time}"