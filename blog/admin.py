from django.contrib import admin
from .models import Post
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


class CommentsAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'content']
    ordering = ['active', 'created']
    date_hierarchy = 'created'
    readonly_fields = ['created', 'updated']