from django.http import (
    Http404,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotAllowed,
    HttpResponseServerError,
    JsonResponse
)
from django.shortcuts import get_object_or_404, render, redirect
from django.core import mail
from django.db.models import Count, Q
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.views import View
from django.views.generic import DetailView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Comment, Post, PublicPostsManager, Tag
from .utils import get_list_of_pagination_pages
from .forms import CommentForm, ShareViaEmailForm, PostForm

DEFAULT_PER_PAGE = 9

def like_post(request, slug):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    post = get_object_or_404(Post, slug=slug)
    post.likes += 1
    post.save()
    return HttpResponse("OK")
def unlike_post(request, slug):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    post = get_object_or_404(Post, slug=slug)
    post.likes -= 1 if post.likes > 0 else 0
    post.save()
    return HttpResponse("OK")

class TagListJSON(View):
    def get(self, request, *args, **kwargs):
        search_term = request.GET.get("search", None)
        if search_term:
            tags = Tag.objects.filter(name__icontains=search_term)
        else:
            tags = Tag.objects.all()
        return JsonResponse(
            {'tags': [{'name': tag.name, 'slug': tag.slug} for tag in tags]},
        )

class CreatePost(LoginRequiredMixin, View):
    login_url = '/admin/login/'
    def get(self, request, *args, **kwargs):
        return render(request, "create_post.html")

    def get_tags_queryset(self):
        if not self.form.cleaned_data['tags']:
            return
        self.tag_names = []
        tags = self.form.cleaned_data['tags']
        for tag in tags:
            if tag['name'] not in self.tag_names:
                self.tag_names.append(tag['name'])
                if not Tag.objects.filter(name=tag['name']).exists():
                    Tag.objects.create(name=tag['name'])

        self.tags = Tag.objects.filter(name__in=self.tag_names)
        return self.tags

    def post(self, request, *args, **kwargs):
        form_data = request.POST
        form_files = request.FILES
        self.form = PostForm(form_data)
        self.action = form_data.get('action', None)
        if self.form.is_valid():
            self.obj = Post(
                title=self.form.cleaned_data['title'],
                body=self.form.cleaned_data['body'],
                author=request.user.author,
                status=Post.Status.PUBLIC if self.action == 'publish' else Post.Status.DRAFT if self.action == 'draft' else None,
                image=form_files['image'] if form_files.get('image', None) else None,
            )
            self.obj.save()
            if self.form.cleaned_data['tags']:
                self.get_tags_queryset()
                for tag in self.tags:
                    self.obj.tags.add(tag)
            return redirect('blog:post_detail', slug=self.obj.slug) if self.action == 'publish' else redirect('blog:create_post')
        else:
            return HttpResponseBadRequest(f'Error with: {self.form.errors} | body: {self.request.POST["body"]}')



class Index(View):
    def get_featured_post(self):
        return Post.publics.first()

    def get_latest_posts(self):
        return Post.publics.all()[:4]

    def get_featured_tags(self):
        # tags with the most posts
        return Tag.objects.annotate(num_posts=Count("posts")).order_by("-num_posts")[:3]
    def get(self, request, *args, **kwargs):
        return render(request, "index.html", context={"posts": Post.publics.all()[:3], "featured_post": self.get_featured_post(), "latest_posts": self.get_latest_posts(), "featured_tags": self.get_featured_tags()})


class PostList(View):
    DEFAULT_PER_PAGE = DEFAULT_PER_PAGE or 9

    def get_pagination(self):
        self.per_page = int(self.request.GET.get("per_page", self.DEFAULT_PER_PAGE))
        self.page_number = int(self.request.GET.get("page", 1))
        self.paginator = Paginator(self.queryset, per_page=self.per_page)
        self.pages = get_list_of_pagination_pages(
            self.page_number, self.paginator.num_pages
        )
        self.next_page = (
            self.page_number + 1
            if self.page_number < self.paginator.num_pages
            else None
        )
        self.prev_page = self.page_number - 1 if self.page_number > 1 else None
        self.pagination_info = {
            "current": self.page_number,
            "per_page": self.per_page,
            "max": self.paginator.num_pages,
            "pages": self.pages,
            "next": self.next_page,
            "prev": self.prev_page,
        }

    def get_paginated_queryset(self):
        if not hasattr(self, "paginator") or not hasattr(self, "page_number"):
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
        additional_context = {}
        if "tag" in kwargs:
            tag = get_object_or_404(Tag, slug=kwargs["tag"])
            self.queryset = tag.posts.filter(status=Post.Status.PUBLIC)
            additional_context["tag"] = tag
        elif "search" in request.GET:
            search_term = request.GET["search"]
            self.queryset = Post.publics.filter(
                Q(title__icontains=search_term) or Q(body__icontains=search_term)
            )
            additional_context["search"] = search_term

        else:
            self.queryset = Post.publics.all()
        posts = self.get_paginated_queryset()
        return render(
            request,
            "post_list.html",
            {"posts": posts, "pagination": self.pagination_info, **additional_context},
        )


class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form_data = request.POST
        form = CommentForm(form_data)
        if form.is_valid():
            data = form.cleaned_data
            name = data["name"]
            email = data["email"]
            content = data["content"]
            Comment.objects.create(name=name, email=email, content=content, post=post)
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.filter(active=True)
        context["form"] = CommentForm()
        context["similar_posts"] = self.get_similar_posts()
        return context

    def get_similar_posts(self):
        tags = self.object.tags.all()
        if not tags:
            return Post.publics.all().exclude(pk=self.object.pk).order_by("-published")[:3]
        mutual_posts = Post.publics.filter(tags__in=tags).exclude(pk=self.object.pk)
        if mutual_posts.count() < 3:
            needed_posts = 3 - mutual_posts.count()
            extra_posts = Post.publics.all().exclude(pk=self.object.pk).order_by("-published")[:needed_posts]
            mutual_posts = mutual_posts | extra_posts
        ordered_posts = mutual_posts.distinct().annotate(num_tags=Count("tags")).order_by(
            "-num_tags", "-published"
        )[:3]
        return ordered_posts


class PostShareEmail(View):
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        form = ShareViaEmailForm(request.POST)
        if form.is_valid():
            try:
                data = form.cleaned_data
                sender_name = data["sender_name"]
                sender_email = data["sender_email"]
                receiver_email = data["receiver_email"]
                subject = f"{sender_name} recommends you read {post.title}"
                html_message = render_to_string(
                    "share_post_email.html",
                    {
                        "post": post,
                        "sender_name": sender_name,
                        "sender_email": sender_email,
                    },
                )
                plain_message = strip_tags(html_message)
                mail.send_mail(
                    subject,
                    plain_message,
                    sender_email,
                    [receiver_email],
                    html_message=html_message,
                )
                return HttpResponse("OK")
            except Exception as e:
                return (
                    HttpResponseServerError(e)
                    if settings.DEBUG
                    else HttpResponseServerError("Internal server error")
                )
        else:
            return HttpResponseBadRequest("Invalid form data")
