from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.utils.text import slugify
from .models import Project

# Create your views here.
def index(request):
    projects = Project.objects.all().order_by('order', '-updated')
    return render(request, "projects.html", {'projects': projects})
