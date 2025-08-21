import os
import requests
import time
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from shared.utils import replace_font_quotes, clean_iframes
from django.core.validators import MaxValueValidator, MinValueValidator
from dotenv import load_dotenv
load_dotenv()  # take environment variables

IGDB_ID = os.getenv('IGDB_ID')
IGDB_SECRET = os.getenv('IGDB_SECRET')

class GameStatus(models.Model):
    # Static enum-like field for game status (fixed options)
    PLAYING = 'Playing'
    COMPLETED = 'Completed'
    DROPPED = 'Dropped'
    PLANNED = 'Planned'
    ONHOLD = 'On Hold'

    STATUS_CHOICES = [
        (PLAYING, 'Playing'),
        (COMPLETED, 'Completed'),
        (DROPPED, 'Dropped'),
        (PLANNED, 'Planned'),
        (ONHOLD, 'On Hold'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PLANNED)
    
    class Meta:
        ordering = ["status"]
        verbose_name = "Status"
        verbose_name_plural = "Status"

    def __str__(self):
        return self.status


class GamePlatform(models.Model):
    # Dynamic model to manage platforms via the admin panel
    platform_name = models.CharField(max_length=100)
    
    class Meta:
        ordering = ["platform_name"]
        verbose_name = "Platform"
        verbose_name_plural = "Platforms"
    
    def __str__(self):
        return self.platform_name


class GameEntry(models.Model):
    game_title = models.CharField(max_length=255)
    status = models.ForeignKey(GameStatus, on_delete=models.PROTECT)  # Relate to GameStatus model
    started = models.DateField(null=True, blank=True)
    finished = models.DateField(null=True, blank=True)  # Allow null if the game isn't finished
    t_rating = models.IntegerField(null=True, blank=True, validators=[
        MaxValueValidator(100),
        MinValueValidator(1)
    ])  # Player's rating
    h_rating = models.IntegerField(null=True, blank=True, validators=[
        MaxValueValidator(100),
        MinValueValidator(1)
    ])  # Player's rating
    initiator = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)
    platform = models.ForeignKey(GamePlatform, null=True, blank=True, on_delete=models.PROTECT)  # Relate to GamePlatform model
    play_time = models.DurationField(null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    igdb_id = models.IntegerField(null=True, blank=True)

    # These fields will be stored but likely managed/updated via IGDB
    genre = models.CharField(null=True, blank=True, max_length=255)
    franchise = models.CharField(null=True, blank=True, max_length=255)
    series = models.CharField(null=True, blank=True, max_length=255)
    estimated_play_time = models.DurationField(null=True, blank=True)
    
    # Auto updating database meta data
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ID: {self.pk} - {self.game_title}"

    class Meta:
        ordering = ["game_title"]
        verbose_name = "Game Entry"
        verbose_name_plural = "Game Entries"
            
    def save(self, *args, **kwargs):
        if self.igdb_id is not None:
            try:
                access_token = self._igdb_get_access_token()
                game_data = self._igdb_query(access_token, "https://api.igdb.com/v4/games", f"fields name, collections.name, genres.name, franchises.name; where id = {self.igdb_id};")
                game_ttb_data = self._igdb_query(access_token, "https://api.igdb.com/v4/game_time_to_beats", f"fields normally; where game_id = {self.igdb_id};")
                
                print("GAME DATA:", game_data)
                print("GAME TTB DATA:", game_ttb_data)
                
                game_name = (game_data or [{}])[0].get("name")
                if(game_name): 
                    self.game_title = game_name
                
                estimated_play_time = (game_ttb_data or [{}])[0].get("normally")
                if isinstance(estimated_play_time, (int, float)):
                    self.estimated_play_time = timedelta(seconds=int(estimated_play_time))
                
                game_series = (game_data or [{}])[0].get("collections") or []
                self.series = " | ".join(x.get("name") for x in game_series if isinstance(x, dict) and x.get("name")) or ""
                
                game_genres = (game_data or [{}])[0].get("genres") or []
                self.genre = " | ".join(x.get("name") for x in game_genres if isinstance(x, dict) and x.get("name")) or ""
                
                game_franchises = (game_data or [{}])[0].get("franchises") or []
                self.franchise = " | ".join(x.get("name") for x in game_franchises if isinstance(x, dict) and x.get("name")) or ""

            except Exception as e:
                print("IGDB fetch failed:", repr(e))
                
        # Clean iframes and replace escaped quotes before saving the body
        self.body = replace_font_quotes(clean_iframes(self.body))
        super().save(*args, **kwargs)
        
    def _igdb_get_access_token(self) -> str:
        if not IGDB_ID or not IGDB_SECRET:
            raise RuntimeError("Missing IGDB_ID / IGDB_SECRET")
    
        url = "https://id.twitch.tv/oauth2/token"
        resp = requests.post(
            url,
            data={
                "client_id": f"{IGDB_ID}",
                "client_secret": f"{IGDB_SECRET}",
                "grant_type": "client_credentials",
            },
            timeout=(3, 10),
        )
        if not resp.ok:
            raise RuntimeError(f"Auth failed: {resp.status_code} {resp.text[:200]}")
        return resp.json()["access_token"]

    def _igdb_query(self, access_token: str, url: str, body: str):
        headers = {
            "Client-ID": f"{IGDB_ID}",
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        }
        max_retries = 5
        backoff = 0.6

        for attempt in range(1, max_retries + 1):
            try:
                resp = requests.post(url, headers=headers, data=body, timeout=(3, 15))
                if resp.status_code == 429:
                    # rate-limited: use Retry-After if provided
                    retry_after = int(resp.headers.get("Retry-After", 1))
                    time.sleep(retry_after)
                    continue
                if not resp.ok:
                    raise RuntimeError(f"IGDB {url} -> {resp.status_code} {resp.text[:200]}")
                return resp.json()
            except Exception as e:
                if attempt == max_retries:
                    raise e
                time.sleep(backoff)
                backoff *= 1.7  # exponential backoff
        
    
        
