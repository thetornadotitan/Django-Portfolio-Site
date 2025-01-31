from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Project, ProjectTags, ProjectLinks
from .forms import ProjectForm

class ProjectAdmin(SummernoteModelAdmin):
    form = ProjectForm  # Use the form with all fields included
    summernote_fields = ('body')  # Explicitly indicate the Summernote field
    filter_horizontal = ('tags', 'links')  # Makes ManyToMany fields user-friendly
    list_display = ('title', 'pk', 'order')  # Add the fields you want to displa
    
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectTags)
admin.site.register(ProjectLinks)