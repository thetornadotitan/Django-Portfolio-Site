from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.utils.text import slugify
from .models import GameEntry

# Create your views here.
def index(request):
    game_entries = GameEntry.objects.all().order_by('game_title')

    # Keep your desired order by pre-seeding keys
    grouped_games = {
        'Playing': [],
        'On Hold': [],
        'Completed': [],
        'Dropped': [],
        'Planned': [],
    }

    def status_key(game):
        # If it's a Django choices field: game.get_status_display()
        if hasattr(game, "get_status_display"):
            return game.get_status_display()
        # If it's an Enum with .label or .value:
        s = getattr(game.status, "label", None) or getattr(game.status, "value", None)
        return s if isinstance(s, str) else str(game.status)

    for game in game_entries:
        key = status_key(game)
        grouped_games.setdefault(key, []).append(game)  # safe even if not pre-seeded

    return render(request, "games.html", {"game_entries": grouped_games})

def game_detail(request, game_entry_id, name=None):
    # Fetch the post by blog_id
    game_entry = get_object_or_404(GameEntry, pk=game_entry_id)
    
    # Generate the slugified title
    slugified_name = slugify(game_entry.game_title)

    # If the title is not provided or doesn't match the slugified title, redirect to the correct URL
    if name != slugified_name:
        return redirect('game_entry', game_entry_id=game_entry.pk, name=slugified_name)

    # Render the post detail page
    return render(request, 'game_entry.html', {'game_entry': game_entry})