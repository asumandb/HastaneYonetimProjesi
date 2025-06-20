from django.db import models
from django.utils.translation import gettext_lazy as _


class Patients(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    image = models.ImageField(upload_to='patients_images/')
    tc_number = models.CharField(max_length=11)
    date_of_birth = models.DateField()

    class Meta:
        verbose_name = _("Hasta")
        verbose_name_plural = _("Hastalar")

    def __str__(self):
        return f"{self.name} {self.surname}"
        return self.email
        return self.phone
        return self.image
        return self.tc_number
        return self.date_of_birth
        return self.id
    
        