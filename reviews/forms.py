from django import forms
from .models import Review
from django.utils.translation import gettext_lazy as _

# Create your forms here.
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'content', 'image']
        # widgets = {
        #     'title': forms.TextInput,
        #     'content': forms.Textarea,
        #     'image': forms.ImageField,
        # }
        # labels = {
        #     'content': _('Content'),
        # }
        # help_texts = {
        #     'content': _('Write the review.')
        # }
        # error_messages = {
        #     'title': {
        #         'max_length': _("The title is too long.")
        #     }
        # }