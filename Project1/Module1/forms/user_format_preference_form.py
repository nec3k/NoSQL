from django import forms
from Module1.models.user_format_preference import UserFormatPreference
from Module1.models.download_format import DownloadFormat

class UserFormatPreferenceForm(forms.ModelForm):
	class Meta:
		model = UserFormatPreference
		fields = ['format']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["format"].queryset = DownloadFormat.objects.filter(enabled=True)