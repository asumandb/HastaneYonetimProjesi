# Hastane Yönetim Sistemi

Django 3.2 ile geliştirilmiş hastane yönetim sistemi.

## Kurulum

1. Sanal ortam oluşturun:
```bash
python -m venv venv
```

2. Sanal ortamı aktifleştirin:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Gereksinimleri yükleyin:
```bash
pip install -r requirements.txt
```

4. Veritabanı migrasyonlarını çalıştırın:
```bash
python manage.py migrate
```

5. Süper kullanıcı oluşturun:
```bash
python manage.py createsuperuser
```

6. Sunucuyu başlatın:
```bash
python manage.py runserver
```

## Özellikler

- Hasta kayıt ve yönetimi
- Doktor kayıt ve yönetimi
- Randevu sistemi
- Poliklinik yönetimi
- Kullanıcı yetkilendirme sistemi 