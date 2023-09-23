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
    # prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published'
    # exclude slug field form forms
    # fields = []
    # exclude = ['slug']
    readonly_fields = ['slug']
