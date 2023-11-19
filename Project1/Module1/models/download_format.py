from django.db import models
from django.core.cache import cache
from django import forms


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

    def get_enabled_formats_as_choices(from_cache = True):
        cachekey = "enabled_format_choices"
        cache_time = 60
        if from_cache:
            result = cache.get(cachekey)
        if not from_cache or result is None:
            result = list(forms.ModelChoiceField(DownloadFormat.objects.filter(enabled=True), empty_label=None).choices)
            cache.set(cachekey, result, cache_time)
        return result
    
    def get_format_from_cache(format_id):
        cachekey = f"downloader_format_id={format_id}"
        cache_time = 60*5
        result = cache.get(cachekey)
        if result is None:
            result = DownloadFormat.objects.get(id=format_id)
            cache.set(cachekey, result, cache_time)
        return result
