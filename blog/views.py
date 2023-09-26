from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseServerError
from django.shortcuts import get_object_or_404, render
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from .models import Post, PublicPostsManager
from .utils import get_list_of_pagination_pages
from .forms import ShareViaEmailForm

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
        page_number = number_of_pages
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
    comments = post.comments.filter(active=True)
    return render(request, 'post_detail.html', {'post': post, 'comments': comments})

def post_share_email(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        print(request.POST)
        form = ShareViaEmailForm(request.POST)
        if form.is_valid():
            try:
                data = form.cleaned_data
                sender_name = data['sender_name']
                sender_email = data['sender_email']
                receiver_email = data['receiver_email']
                subject = f'{sender_name} recommends you read {post.title}'
                html_message = render_to_string('share_post_email.html', {'post': post, 'sender_name': sender_name, 'sender_email': sender_email})
                plain_message = strip_tags(html_message)
                mail.send_mail(subject, plain_message, sender_email, [receiver_email], html_message=html_message)
                return HttpResponse('OK')
            except Exception as e:
                raise e
                return HttpResponseServerError(e) if settings.DEBUG else HttpResponseServerError('Internal server error')
        else :
            return HttpResponseBadRequest('Invalid form data')
    else:
        return HttpResponseNotAllowed(['POST'])



