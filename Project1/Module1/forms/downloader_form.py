from collections.abc import Mapping
from typing import Any
from django import forms
from django.forms import Textarea
from django.forms.utils import ErrorList
from Module1.models.download_format import DownloadFormat
from django.core.cache import cache

class DownloaderForm(forms.Form):
    content = forms.CharField(label="Odkazy", max_length=25600, widget=Textarea(attrs={"rows": 8, "class": "textarr"}))
    playlist = forms.BooleanField(required=False, initial=False, label='Playlist', label_suffix="")
    format = forms.ModelChoiceField(label="Formát", queryset=DownloadFormat.objects.filter(enabled=True), initial=1)
    #format = forms.ChoiceField()

    #def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    self.fields["format"] = forms.ChoiceField(label="Formát", choices=DownloadFormat.get_enabled_formats_as_choices(), initial=1)
