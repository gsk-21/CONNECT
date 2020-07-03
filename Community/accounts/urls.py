from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('login/', auth_views.LoginView.as_view(template_name='users/login.html',
                                                extra_context={'logged_in':1}), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('sign-up/', views.sign_up, name='sign-up'),

    path('my-profile/', views.UserProfile.as_view(), name='my-profile'),

    path('my-profile/update-profile-pic/', views.update_profile_pic, name='update-profile-pic'),

    path('my-profile/delete-profile-pic/', views.delete_profile_pic, name='delete-profile-pic'),

    path('my-profile/update-profile-details/', views.update_profile_details, name='update-profile-details'),

    path('about-user/<int:pk>', views.about_user, name='about-user'),

    path('notifications/', views.notifications, name='notifications'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

    # path('about-user/<int:pk>/',views.AboutUser.as_view(),name = 'about-user')
