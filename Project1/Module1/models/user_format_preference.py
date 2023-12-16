from django.db import models
from django.contrib.auth.models import User
from Module1.models.download_format import DownloadFormat

class UserFormatPreference(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, null=False, verbose_name="Uživatel", on_delete=models.CASCADE)
    format = models.ForeignKey(DownloadFormat, null=True, verbose_name="Preferovaný formát", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Uživatel: {self.user} preferuje {self.format}. "
    
    