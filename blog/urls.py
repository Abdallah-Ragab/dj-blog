from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('posts/new/', views.CreatePost.as_view(), name='create_post'),
    path('posts/', views.PostList.as_view(), name='post_list'),
    path('posts/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/<slug:slug>/share/email', views.PostShareEmail.as_view(), name='post_share_email'),
    path('tags/<slug:tag>/', views.PostList.as_view(), name='tag_list'),
    path('tags/', views.TagListJSON.as_view(), name='tag_list_json'),
]