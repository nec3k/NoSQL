# NoSQL

## YouTube Downloader s Django a Celery

Tento projekt umožňuje stahovat audio/video z YouTube pomocí aplikace postavené na Django a Celery. Před spuštěním si prosím přečtěte následující pokyny.

### Instalace

1. Spusťte projekt pomocí příkazu `docker-compose up`.

2. Vytvořte si vlastního superuživatele v Django kontejneru pomocí příkazu:

```bash
python manage.py createsuperuser
```

### Resetování Hesla

Aby byla funkce resetu hesla plně funkční, nastavte parametry pro SMTP klienta v souboru `Project1/Project1/settings.py`.

```python
# Project1/Project1/settings.py

EMAIL_HOST = 'smtp.seznam.cz'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'user@example.com'
EMAIL_HOST_PASSWORD = 'secret'
EMAIL_USE_SSL = True
```
