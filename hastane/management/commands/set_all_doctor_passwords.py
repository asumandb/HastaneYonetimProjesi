from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from hastane.models.doctors_model import Doctors

class Command(BaseCommand):
    help = 'Tüm doktorlara şifre atar.'

    def add_arguments(self, parser):
        parser.add_argument('--password', type=str, default='123456', help='Atanacak şifre (varsayılan: 123456)')

    def handle(self, *args, **options):
        password = options['password']
        
        doctors = Doctors.objects.all()
        
        if not doctors.exists():
            self.stdout.write(self.style.WARNING('Veritabanında doktor bulunamadı!'))
            return
        
        self.stdout.write(f'Tüm doktorlara "{password}" şifresi atanıyor...')
        
        for doctor in doctors:
            doctor.password = make_password(password)
            doctor.save()
            self.stdout.write(
                self.style.SUCCESS(f'{doctor.name} {doctor.surname} ({doctor.email}) için şifre atandı.')
            )
        
        self.stdout.write(self.style.SUCCESS(f'\nToplam {doctors.count()} doktora şifre atandı.'))
        self.stdout.write(self.style.SUCCESS(f'Giriş bilgileri:'))
        self.stdout.write(self.style.SUCCESS(f'Email: doktor_email_adresi'))
        self.stdout.write(self.style.SUCCESS(f'Şifre: {password}')) 