from django.db import models
from django.utils.translation import gettext_lazy as _


class Clinic(models.Model):
    name = models.CharField(_("Medora"),max_length=100, unique=True)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    website = models.URLField(max_length=100)
    image = models.ImageField(upload_to='clinic_images/')

    class Meta:
        verbose_name = _("Klinik")
        verbose_name_plural = _("Klinikler")

    def __str__(self):
        return self.name
        return self.address
        return self.phone
        return self.email
        return self.website
        return self.image
        return self.id
