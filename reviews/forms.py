from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import SuspiciousOperation

from .models import Review

# Create your forms here.
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Title'
                },
            ),
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control'
                },
            ),
            'image': forms.FileInput(
                attrs={
                    'accept': 'image/*',
                    'class': 'form-control-file',
                    'id': 'file_image'
                },
            )
        }
        labels = {
            'content': _('Content'),
        }
        help_texts = {
            'content': _('Write the review.')
        }
        error_messages = {
            'title': {
                'max_length': _("The title is too long.")
            }
        }
