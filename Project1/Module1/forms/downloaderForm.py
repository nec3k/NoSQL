from django import forms
from django.forms import Textarea
from Module1.models.download_format import DownloadFormat


class DownloaderForm(forms.Form):
    content = forms.CharField(label="Odkazy", max_length=25600, widget=Textarea(attrs={"rows": 8, "class": "textarr"}))
    playlist = forms.BooleanField(required=False, initial=False, label='Playlist', label_suffix="")
    format = forms.ModelChoiceField(label="Formát", queryset=DownloadFormat.objects.filter(enabled=True,), initial=1)
