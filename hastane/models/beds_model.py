from django.db import models

class Beds(models.Model):
    number = models.CharField(max_length=10, verbose_name="Yatak Numarası")
    room = models.CharField(max_length=50, verbose_name="Oda")
    status = models.CharField(
        max_length=20,
        choices=[('boş', 'Boş'), ('dolu', 'Dolu')],
        default='boş',
        verbose_name="Durum"
    )

    def __str__(self):
        return f"{self.number} - {self.room} ({self.status})"