from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from hastane.models.doctors_model import Doctors

class Command(BaseCommand):
    help = 'Belirli bir doktor için belirli bir şifre atar.'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Doktorun email adresi')
        parser.add_argument('password', type=str, help='Atanacak şifre')

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']
        
        try:
            doctor = Doctors.objects.get(email=email)
            doctor.password = make_password(password)
            doctor.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'{doctor.name} {doctor.surname} için şifre "{password}" olarak ayarlandı.')
            )
        except Doctors.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'{email} email adresi ile doktor bulunamadı!')
            ) 