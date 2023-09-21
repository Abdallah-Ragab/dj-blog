from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.contrib.auth import get_user_model

USER = get_user_model()
# Create your models here.

class PublicPostsManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(status=Post.Status.PUBLIC)

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLIC = 'PB', 'Public'
        ARCHIVED = 'AC', 'Archived'


    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    body = models.TextField()
    status = models.CharField(choices=Status.choices, max_length=2, default=Status.DRAFT)
    author = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="posts")
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    objects = models.Manager()
    publics = PublicPostsManager()

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['-published']
        indexes = [
            models.Index(fields=['-published'],            )
        ]