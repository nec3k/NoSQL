from django.db import models
from django.contrib.auth.models import User
from Module1.models.download_format import DownloadFormat

class DownloadRequest(models.Model):
    REQUEST_STATES = [
        ('SUCCESS','ÚSPĚCH'),
        ('PROCESSING','ZPRACOVÁVÁNÍ'),
        ('IN_QUEUE','VE FRONTĚ'),
        ('DOWNLOADER ERROR','CHYBA STAHOVÁNÍ'),
        ('CRITICAL ERROR','KRITICKÁ CHYBA'),
    ]
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=512, null=False, verbose_name="URL")
    start_datetime = models.DateTimeField(null=False, verbose_name="Datum START", auto_now_add=True)
    finish_datetime = models.DateTimeField(null=True, verbose_name="Datum FINISH", auto_now_add=False)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, verbose_name="Uživatel")
    state = models.CharField(null=False, verbose_name="Stav požadavku", choices=REQUEST_STATES, default="IN_QUEUE")
    format = models.ForeignKey(DownloadFormat, null=False, verbose_name="Formát", on_delete=models.RESTRICT)

    def state_css_class(self):
        if self.state == 'SUCCESS':
            return 'success'
        elif self.state == 'PROCESSING':
            return 'warning'
        elif self.state == 'IN_QUEUE':
            return 'info'
        elif self.state == 'DOWNLOADER ERROR' or 'CRITICAL ERROR':
            return 'danger'
        else:
            return 'secondary'

    def __str__(self) -> str:
        return f"Požadavek id: {self.id}, založil: {self.user} ({self.start_datetime.strftime('%Y-%m-%d %H:%M')})"
