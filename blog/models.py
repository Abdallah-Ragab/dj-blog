from django.urls import reverse
from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.contrib.auth import get_user_model
from .utils import generate_unique_slug
from django.db.models.signals import pre_save

USER = get_user_model()
AUTO_COMMENT_ACTIVE = True

def save_image(instance, filename):
    return f"images/{instance.author}-{filename}"

class Author(models.Model):
    user = models.OneToOneField(USER, on_delete=models.CASCADE, related_name="author")
    bio = models.TextField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to="images/", blank=True, null=True)

    def __str__(self) -> str:
        return self.user.username

class Tag(models.Model):
    name = models.CharField(max_length=24)
    slug = models.SlugField(max_length=24, unique=True, blank=True, null=True)
    description = models.TextField(max_length=128, blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("blog:tag_list", kwargs={"tag": self.slug})

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(
                fields=["name"],
            )
        ]

class Comment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=50)
    content = models.TextField(max_length=500)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=AUTO_COMMENT_ACTIVE)

    def __str__(self) -> str:
        return f"Comment by {self.name}:{self.email} on {self.post} at {self.created}"

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(
                fields=["-created", "post", "active"],
            )
        ]

class PublicPostsManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(status=Post.Status.PUBLIC)

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLIC = "PB", "Public"
        ARCHIVED = "AC", "Archived"

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    body = models.TextField()
    status = models.CharField(
        choices=Status.choices, max_length=2, default=Status.DRAFT
    )
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="posts")
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name="posts")
    image = models.ImageField(upload_to=save_image, blank=True, null=False, default="media/default.jpg")
    likes = models.IntegerField(default=0)

    objects = models.Manager()
    publics = PublicPostsManager()

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-published"]
        indexes = [
            models.Index(
                fields=["-published"],
            )
        ]

def auto_populate_unique_slug(sender, instance, update_fields, *args, **kwargs):
    instance.slug = generate_unique_slug(Post, "slug", "title", instance)

def auto_populate_unique_slug_for_tag(sender, instance, update_fields, *args, **kwargs):
    instance.slug = generate_unique_slug(Tag, "slug", "name", instance)


pre_save.connect(auto_populate_unique_slug, sender=Post)
pre_save.connect(auto_populate_unique_slug_for_tag, sender=Tag)