from django import forms
from django_summernote.fields import SummernoteTextField
from .models import Project

class ProjectForm(forms.ModelForm):
    # Apply SummernoteTextField with sanitization to the body field
    body = SummernoteTextField()

    class Meta:
        model = Project
        fields = '__all__'  # Include all fields from the model