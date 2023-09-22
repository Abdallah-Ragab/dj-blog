from django.http import Http404
from django.shortcuts import get_object_or_404, render
from .models import Post
# Create your views here.

def post_list(request):
    posts = Post.publics.all()
    return render(request, 'post_list.html', {'posts': posts})

def post_detail(request, id):
    post = get_object_or_404(Post, id=id, status='published')
    # try:
    #     post = Post.publics.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404('Post not found')
    return render(request, 'post_detail.html', {'post': post})
