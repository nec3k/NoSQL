from django.contrib import admin
from Module1.models import DownloadFormat
from Module1.models import DownloadedFile
from Module1.models import DownloadRequest
from Module1.models import UserFormatPreference
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
    list_display = ['id', 'url', 'task_status', 'task_date_created', 'task_date_done', 'user', 'files_downloaded','format']
    list_filter = ('user','task__status', 'task__date_created', 'task__date_done')

class UserFormatPreferenceAdmin (admin.ModelAdmin):
    list_display = ['id', 'user', 'format']
    list_filter = ('format',)

    
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
admin.site.register(UserFormatPreference, UserFormatPreferenceAdmin)


