from django.contrib import admin
from .models import Post, Comment, Tag
# Register your models here.

# admin.site.register(Post)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published', 'status']
    list_filter = ['author', 'published', 'status']
    list_editable = ['status']
    search_fields = ['title', 'body']
    ordering = ['status', 'published']
    date_hierarchy = 'published'
    readonly_fields = ['slug']

@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'post']
    search_fields = ['name', 'email', 'content']
    ordering = ['active', 'created', 'post']
    date_hierarchy = 'created'

@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']
    ordering = ['name']
    readonly_fields = ['slug']
