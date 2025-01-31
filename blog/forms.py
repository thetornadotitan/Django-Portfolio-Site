from django import forms
from django_summernote.fields import SummernoteTextField
from .models import BlogPost

class BlogPostForm(forms.ModelForm):
    # Apply SummernoteTextField with sanitization to the body field
    summary = SummernoteTextField()
    body = SummernoteTextField()

    class Meta:
        model = BlogPost
        fields = '__all__'  # Include all fields from the model