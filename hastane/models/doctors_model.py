from django.db import models
from django.utils.translation import gettext_lazy as _

class Doctors(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='doctors_images/')
    speciality = models.CharField(max_length=100)

    class Meta:
        verbose_name = _("Doktor")
        verbose_name_plural = _("Doktorlar")

    def __str__(self):
        return f"{self.name} {self.surname}, {self.speciality}"
        return self.email
        return self.phone
        return self.clinic
        return self.id
