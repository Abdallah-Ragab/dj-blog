from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('posts/', views.PostList.as_view(), name='post_list'),
    path('posts/<slug:slug>/', views.post_detail, name='post_detail'),
    path('posts/<slug:slug>/share/email', views.post_share_email, name='post_share_email'),
    # path('tags/<slug:slug>/', views.tag_detail, name='tag_detail'),
]