from django.db import models
from django.contrib.auth.models import User
from Module1.models.download_format import DownloadFormat
from django_celery_results.models import TaskResult

MAX_URL_LENGTH = 512

class DownloadRequest(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=MAX_URL_LENGTH, null=False, verbose_name="URL")
    task = models.ForeignKey(TaskResult, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, verbose_name="Uživatel")
    format = models.ForeignKey(DownloadFormat, null=False, verbose_name="Formát", on_delete=models.RESTRICT)

    @property
    def task_status(self):
        return self.task.status if self.task is not None else None
    
    @property
    def task_date_created(self):
        return self.task.date_created if self.task is not None else None
    
    @property
    def task_date_done(self):
        return self.task.date_done if self.task is not None else None
    
    @property
    def files_downloaded(self):
        from Module1.models.downloaded_file import DownloadedFile
        files = DownloadedFile.objects.filter(request=self)
        files_str = ";".join([soubor.filename for soubor in files])
        return files_str

    def as_dict(self):
        return {"id": self.id,
                "url": self.url,
                "task": self.task.as_dict,
                "user__username": self.user.username,
                "format__file_type": self.format.file_type}
    
    def __str__(self) -> str:
        return f"Požadavek id: {self.id}, založil: {self.user}"
