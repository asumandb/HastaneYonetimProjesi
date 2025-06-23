from django.db import models

class Rooms(models.Model):
    number = models.CharField(max_length=10, verbose_name="Oda Numarası", unique=True)
    status = models.CharField(
        max_length=20,
        choices=[('boş', 'Boş'), ('dolu', 'Dolu')],
        default='boş',
        verbose_name="Durum"
    )
    room_type = models.CharField(max_length=10, choices=[('tek', 'Tek Kişilik'), ('cift', 'Çift Kişilik')], default='tek')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.number} - {self.room} ({self.status})"