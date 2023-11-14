from django.db import models
from django.core.cache import cache


class DownloadFormat(models.Model): 
    FILE_TYPES = [("audio", "Audio"), ("video", "Video")]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, null=False, verbose_name="Název formátu")
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name="Popis")
    enabled = models.BooleanField(null=False, verbose_name="Povolen", default=False)
    yt_dl_opts = models.JSONField(null=True, blank=True) 
    file_type = models.CharField(null=True, verbose_name="Typ souboru", choices=FILE_TYPES)
    
    def __str__(self) -> str:
        return self.name

