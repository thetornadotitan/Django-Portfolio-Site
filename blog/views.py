from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.utils.text import slugify
from .models import BlogPost

# Create your views here.
def index(request):
    posts = BlogPost.objects.all().order_by('-updated')
    return render(request, "blog.html", {'posts': posts})

def blog_detail(request, blog_id, title=None):
    # Fetch the post by blog_id
    post = get_object_or_404(BlogPost, pk=blog_id)
    
    # Generate the slugified title
    slugified_title = slugify(post.title)

    # If the title is not provided or doesn't match the slugified title, redirect to the correct URL
    if title != slugified_title:
        return redirect('blog_detail', blog_id=post.pk, title=slugified_title)

    # Render the post detail page
    return render(request, 'blog_detail.html', {'post': post})