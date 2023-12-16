from django import forms


class FileForm(forms.Form):
	def __init__(self, file_list, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["files"] = forms.MultipleChoiceField(choices=file_list, widget=forms.CheckboxSelectMultiple, required=False)

	files = forms.MultipleChoiceField()
