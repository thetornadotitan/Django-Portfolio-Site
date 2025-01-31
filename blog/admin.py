from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import BlogPost
from .forms import BlogPostForm

class BlogPostAdmin(SummernoteModelAdmin):
    form = BlogPostForm  # Use the form with all fields included
    summernote_fields = ('body','summary',)  # Explicitly indicate the Summernote field
    
admin.site.register(BlogPost, BlogPostAdmin)