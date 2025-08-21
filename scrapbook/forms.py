from django import forms
from django_summernote.fields import SummernoteTextField
from .models import GameEntry

class GameEntryForm(forms.ModelForm):
    # Apply SummernoteTextField with sanitization to the body field
    body = SummernoteTextField()

    class Meta:
        model = GameEntry
        fields = '__all__'  # Include all fields from the model