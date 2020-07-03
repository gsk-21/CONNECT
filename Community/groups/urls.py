from django.urls import path
from . import views

urlpatterns = [

    path('create-community/', views.create_community, name='create-community'),

    path('communities/', views.CommunityList.as_view(), name='communities'),

    path('communities/<slug:slug>/', views.CommunityDetail.as_view(), name='community-detail'),

    path('join-community/<slug:slug>/', views.join_community, name='join-community'),

    path('exit-community/<slug:slug>/', views.exit_community, name='exit-community'),

    path('my-profile/my-communities', views.MyCommunityList.as_view(), name='my-communities'),

    path('my-profile/following-communities', views.FollowingCommunityList.as_view(), name='following-communities'),

    path('user-following-community/<int:pk>/', views.user_following_community, name='user-following-community'),

    path('user-created-community/<int:pk>/', views.user_created_community, name='user-created-community'),

    path('remove-community-profile/<slug:slug>/', views.remove_community_profile_pic,
         name='remove-community-profile-pic'),

    path('update-community-pic/', views.update_community_pic, name='update-community-pic'),

    path('delete-community/<slug:slug>/', views.DeleteCommunity.as_view(), name='delete-community'),

]
