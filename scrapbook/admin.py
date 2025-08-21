from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import GameEntry, GamePlatform, GameStatus
from .forms import GameEntryForm

class GameEntryAdmin(SummernoteModelAdmin):
    form = GameEntryForm  # Use the form with all fields included
    summernote_fields = ('body')  # Explicitly indicate the Summernote field
    
admin.site.register(GameEntry, GameEntryAdmin)
admin.site.register(GameStatus)
admin.site.register(GamePlatform)