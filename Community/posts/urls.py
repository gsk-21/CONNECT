from django.urls import path
from . import views

urlpatterns = [

    path('create-post/', views.create_post, name='create-post'),

    path('all-post/', views.AllPosts.as_view(), name='all-posts'),

    path('my-posts/', views.MyPosts.as_view(), name='my-posts'),

    path('post-detail/<slug:slug>/', views.post_detail, name='post-detail'),

    path('delete-post/', views.delete_post, name='delete-post'),

    path('add-comment/', views.add_comment, name='add-comment'),

    path('delete-comment/', views.delete_comment, name='delete-comment'),

    path('reply-comment/', views.reply_comment, name='reply-comment'),

    path('delete-reply/', views.delete_reply, name='delete-reply'),

    path('like/', views.like_toggle, name='like'),

]
