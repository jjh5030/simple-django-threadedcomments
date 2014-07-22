from django import forms
from .models import ThreadedComment


class CommentForm(forms.ModelForm):
	parent_id = forms.CharField(widget=forms.HiddenInput(attrs={'class': 'parent_id'}), required=False)

	class Meta:
		model = ThreadedComment
		fields = ('comment',)