from django.urls import path, re_path
from . import views

urlpatterns = [
    path("scrapbook/", views.index, name="scrapbook"),
    re_path(r'^scrapbook/(?P<game_entry_id>\d+)(?:/(?P<name>[-\w]+))?/$', views.game_detail, name='game_entry'),
]