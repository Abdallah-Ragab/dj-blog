from django.http import Http404
from django.shortcuts import get_object_or_404, render
from .models import Post, PublicPostsManager
# Create your views here.

def post_list(request):
    posts = Post.publics.all()
    return render(request, 'post_list.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.Status.PUBLIC)
    return render(request, 'post_detail.html', {'post': post})
