from django.db import models
from django.utils.translation import gettext_lazy as _
from hastane.models.patients_model import Patients

class Bills(models.Model):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE, related_name="faturalar", verbose_name=_("Hasta"))
    payment = models.DecimalField(_("Tutar"), max_digits=10,decimal_places=2)
    payment_date = models.DateField(_("Ödeme Tarihi"), help_text="Ödeme tarihini giriniz.")
    payment_status = models.BooleanField(_("Ödendi mi?"), default=False)

    class Meta:
        verbose_name = "Fatura"
        verbose_name_plural = "Faturalar"

    def __str__(self):
        return f"Fatura: {self.hasta} - {self.tutar} ₺"