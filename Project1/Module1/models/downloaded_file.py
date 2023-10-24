from django.db import models
from Module1.models.download_request import DownloadRequest

class DownloadedFile(models.Model):
    id = models.AutoField(primary_key=True)
    filename = models.CharField(max_length=256, null=False, verbose_name="Název souboru")
    request = models.ForeignKey(DownloadRequest, null=False, verbose_name="Požadavek", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.filename
    
    