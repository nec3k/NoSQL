from django.contrib import admin
from Module1.models.download_format import DownloadFormat
from Module1.models.downloaded_file import DownloadedFile
from Module1.models.download_request import DownloadRequest
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import format_html

# Register your models here.


class DownloadFormatAdmin (admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'enabled', 'yt_dl_opts', 'file_type']
    list_filter = ('enabled', 'file_type')

class DownloadedFileAdmin (admin.ModelAdmin):
    list_display = ['id', 'filename', 'request_id', ]
    search_fields = ['filename']

class DownloadRequestAdmin (admin.ModelAdmin):
    list_display = ['id', 'url', 'start_datetime', 'finish_datetime', 'user', 'state','display_files','format']
    list_filter = ('state','user','start_datetime', 'finish_datetime')

    def display_files(self, obj):
        files = DownloadedFile.objects.filter(request_id=obj)
        files_str = ";".join([soubor.filename for soubor in files])
        return files_str
    
    display_files.short_description = 'Soubory'
    
# Rozšíření třídy UserAdmin
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'files_link')

    def files_link(self, obj):
        url = reverse('file_manager')
        files_link = format_html(f'<a href="{url}?username={obj.username}">link</a>')
        return files_link

    files_link.short_description = 'Stažené soubory'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


admin.site.register(DownloadFormat, DownloadFormatAdmin)
admin.site.register(DownloadedFile, DownloadedFileAdmin)
admin.site.register(DownloadRequest, DownloadRequestAdmin)


