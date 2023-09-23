from django.http import Http404
from django.shortcuts import get_object_or_404, render
from .models import Post, PublicPostsManager
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .utils import get_list_of_pagination_pages
# Create your views here.
DEFAULT_PER_PAGE = 9

def post_list(request):
    per_page = int(request.GET.get('per_page', DEFAULT_PER_PAGE))
    page_number = int(request.GET.get('page', 1))
    all_posts = Post.publics.all()
    paginator = Paginator(all_posts, per_page=per_page)
    number_of_pages = paginator.num_pages
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(number_of_pages)
    except (PageNotAnInteger, ValueError):
        posts = paginator.page(1)
    pagination_info = {
        'current': page_number,
        'per_page': per_page,
        'max': number_of_pages,
        'pages': get_list_of_pagination_pages(page_number, number_of_pages),
        'next': page_number + 1 if page_number < number_of_pages else None,
        'prev': page_number - 1 if page_number > 1 else None,
    }
    return render(request, 'post_list.html', {'posts': posts, "pagination": pagination_info})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.Status.PUBLIC)
    return render(request, 'post_detail.html', {'post': post})
