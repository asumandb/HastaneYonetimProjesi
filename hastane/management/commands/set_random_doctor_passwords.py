import string
import random
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from hastane.models.doctors_model import Doctors

def generate_password(length=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

class Command(BaseCommand):
    help = 'Her doktora rastgele şifre atar ve şifreleri bir dosyaya kaydeder.'

    def handle(self, *args, **options):
        with open('doctor_passwords.txt', 'w', encoding='utf-8') as f:
            for doctor in Doctors.objects.all():
                raw_password = generate_password()
                doctor.password = make_password(raw_password)
                doctor.save()
                f.write(f"{doctor.name} {doctor.surname} ({doctor.email}): {raw_password}\n")
                self.stdout.write(self.style.SUCCESS(f"{doctor.name} {doctor.surname} için şifre atandı."))
        self.stdout.write(self.style.SUCCESS("Tüm şifreler doctor_passwords.txt dosyasına kaydedildi."))