from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseServerError
from django.shortcuts import get_object_or_404, render
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.views import View
from .models import Comment, Post, PublicPostsManager, Tag
from .utils import get_list_of_pagination_pages
from .forms import CommentForm, ShareViaEmailForm

DEFAULT_PER_PAGE = 9

class PostList(View):
    DEFAULT_PER_PAGE = DEFAULT_PER_PAGE or 9
    def get_pagination(self):
        self.per_page = int(self.request.GET.get('per_page', self.DEFAULT_PER_PAGE))
        self.page_number = int(self.request.GET.get('page', 1))
        self.paginator = Paginator(self.queryset, per_page=self.per_page)
        self.pages = get_list_of_pagination_pages(self.page_number, self.paginator.num_pages)
        self.next_page = self.page_number + 1 if self.page_number < self.paginator.num_pages else None
        self.prev_page = self.page_number - 1 if self.page_number > 1 else None
        self.pagination_info = {
            'current': self.page_number,
            'per_page': self.per_page,
            'max': self.paginator.num_pages,
            'pages': self.pages,
            'next': self.next_page,
            'prev': self.prev_page,
        }

    def get_paginated_queryset(self):
        if not hasattr(self, 'paginator') or not hasattr(self, 'page_number'):
            self.get_pagination()
        try:
            queryset = self.paginator.page(self.page_number)
        except EmptyPage:
            queryset = self.paginator.page(self.paginator.num_pages)
            self.page_number = self.paginator.num_pages
        except (PageNotAnInteger, ValueError):
            queryset = self.paginator.page(1)
        return queryset


    def get(self, request, *args, **kwargs):
        tag_info = {}
        if 'tag' in kwargs:
            tag = get_object_or_404(Tag, slug=kwargs['tag'])
            self.queryset = tag.posts.filter(status=Post.Status.PUBLIC)
            tag_info = {'tag': tag}
        else:
            self.queryset = Post.publics.all()
        posts = self.get_paginated_queryset()
        return render(request, 'post_list.html', {'posts': posts, "pagination": self.pagination_info, **tag_info})

# def tag_detail(request, slug):
#     per_page = int(request.GET.get('per_page', DEFAULT_PER_PAGE))
#     page_number = int(request.GET.get('page', 1))
#     tag = get_object_or_404(Tag, slug=slug)
#     all_posts = tag.posts.filter(status=Post.Status.PUBLIC)
#     paginator = Paginator(all_posts, per_page=per_page)
#     number_of_pages = paginator.num_pages
#     try:
#         posts = paginator.page(page_number)
#     except EmptyPage:
#         posts = paginator.page(number_of_pages)
#         page_number = number_of_pages
#     except (PageNotAnInteger, ValueError):
#         posts = paginator.page(1)
#     pagination_info = {
#         'current': page_number,
#         'per_page': per_page,
#         'max': number_of_pages,
#         'pages': get_list_of_pagination_pages(page_number, number_of_pages),
#         'next': page_number + 1 if page_number < number_of_pages else None,
#         'prev': page_number - 1 if page_number > 1 else None,
#     }
#     return render(request, 'post_list.html', {'tag': tag, 'posts': posts, "pagination": pagination_info})

# def post_list(request):
#     per_page = int(request.GET.get('per_page', DEFAULT_PER_PAGE))
#     page_number = int(request.GET.get('page', 1))
#     all_posts = Post.publics.all()
#     paginator = Paginator(all_posts, per_page=per_page)
#     number_of_pages = paginator.num_pages
#     try:
#         posts = paginator.page(page_number)
#     except EmptyPage:
#         posts = paginator.page(number_of_pages)
#         page_number = number_of_pages
#     except (PageNotAnInteger, ValueError):
#         posts = paginator.page(1)
#     pagination_info = {
#         'current': page_number,
#         'per_page': per_page,
#         'max': number_of_pages,
#         'pages': get_list_of_pagination_pages(page_number, number_of_pages),
#         'next': page_number + 1 if page_number < number_of_pages else None,
#         'prev': page_number - 1 if page_number > 1 else None,
#     }
#     return render(request, 'post_list.html', {'posts': posts, "pagination": pagination_info})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.Status.PUBLIC)
    if request.method == 'POST':
        form_data = request.POST
        form = CommentForm(form_data)
        if form.is_valid():
            data = form.cleaned_data
            name = data['name']
            email = data['email']
            content = data['content']
            Comment.objects.create(name=name, email=email, content=content, post=post)

    comments = post.comments.filter(active=True)
    comment_form = CommentForm()

    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'form': comment_form})

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



