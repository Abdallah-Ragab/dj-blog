from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('posts/', views.PostList.as_view(), name='post_list'),
    path('posts/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/<slug:slug>/share/email', views.post_share_email, name='post_share_email'),
    path('tags/<slug:tag>/', views.PostList.as_view(), name='tag_list'),
]