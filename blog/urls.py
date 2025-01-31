from django.urls import path, re_path
from . import views

urlpatterns = [
    path("blog/", views.index, name="blog"),
    re_path(r'^blog/(?P<blog_id>\d+)(?:/(?P<title>[-\w]+))?/$', views.blog_detail, name='blog_detail'),
]