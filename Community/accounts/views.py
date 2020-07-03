from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Profile
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.http import HttpResponse
from posts.models import Post, Comment, Reply, PostLike
from groups.models import Group, GroupMember
from django.db.models import Q

from django import forms
from itertools import chain
from operator import attrgetter
from django.contrib.auth import login, authenticate
from django.db.models import DateTimeField


# Create your views here.


def home(request):
    context = {}
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user_feeds = posts.filter(group__members=request.user)
        context['has_community'] = 1
        if len(user_feeds) == 0:
            context['has_community'] = 0
            user_feeds = Post.objects.all()
        context['non_following_posts'] = posts.filter(~Q(group__members=request.user))
        context['home_posts'] = user_feeds
    else:
        context['home_posts'] = Post.objects.all()
    context['profiles'] = Profile.objects.all().order_by('joined_on').reverse()
    context['home_communities'] = Group.objects.all()
    return render(request, 'index.html', context)


def validate_email_unique(value):
    exists = User.objects.filter(email=value)
    if exists:
        return 1


def validate_username_unique(value):
    exists = User.objects.filter(username=value)
    if exists:
        return 1


def sign_up(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')
        email = request.POST.get('email')
        confirm_password = request.POST.get('confirm-password')

        context = {'username': username, 'name': name, 'email': email}

        if validate_email_unique(email):
            context['error'] = 'Email already exists'
            return render(request, 'users/sign-up.html', context)

        if validate_username_unique(username):
            context['error'] = 'Username taken'
            return render(request, 'users/sign-up.html', context)

        if len(password) < 8:
            context['error'] = 'Make sure your password contains at least 8 characters'
            return render(request, 'users/sign-up.html', context)

        if password != confirm_password:
            context['error'] = 'Password mismatch'
            return render(request, 'users/sign-up.html', context)

        user = User.objects.create_user(username=username, password=password, email=email, first_name=name)
        profile = Profile()
        profile.user = user
        profile.save()
        return redirect('login')
    else:
        return render(request, 'users/sign-up.html', {})


class UserProfile(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'users/user-profile.html'
    model = Profile
    context_object_name = 'profile'
    template_name = 'users/user-profile.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfile, self).get_context_data(**kwargs)
        context['my_posts'] = Post.objects.filter(author=self.request.user)
        context['created_communities'] = Group.objects.filter(created_by=self.request.user).count
        context['following_communities'] = GroupMember.objects.filter(user=self.request.user).count
        return context


def about_user(request, pk):
    user = User.objects.get(pk=pk)
    print(user)

    context = {}

    context['about_user'] = user
    context['my_posts'] = Post.objects.filter(author=user)
    context['created_communities'] = Group.objects.filter(created_by=user).count
    context['following_communities'] = GroupMember.objects.filter(user=user).count

    return render(request, 'users/about-user-page.html', context)


@login_required
def update_profile_pic(request):
    try:

        if request.method == 'POST':
            new_profile_pic = request.FILES['new-profile-pic']
            profile = Profile.objects.get(user=request.user)
            profile.profile_pic = new_profile_pic
            profile.save(update_fields=['profile_pic'])

        else:
            return HttpResponse("Nope")

    except:

        return HttpResponse("You can't do that!")
    return redirect('my-profile')


@login_required
def delete_profile_pic(request):
    try:
        profile = Profile.objects.get(user=request.user)
        profile.profile_pic.delete(save=True)
        # profile.save(update_fields=['profile_pic'])
    except:
        return HttpResponse("You can't do that!")
    return redirect('my-profile')


@login_required
def update_profile_details(request):
    try:
        password = request.POST.get('password')
        un = request.user.username
        authenticated = authenticate(username=un, password=password)

        if authenticated:
            if request.method == 'POST':
                user = User.objects.get(pk=request.user.pk)
                user.first_name = request.POST.get('new-name')
                user.save(update_fields=['first_name'])

                if 'new-profile-pic' in request.FILES:
                    new_profile_pic = request.FILES['new-profile-pic']
                    profile = Profile.objects.get(user=request.user)
                    profile.profile_pic = new_profile_pic
                    profile.save(update_fields=['profile_pic'])
            else:
                return HttpResponse("Nope")
        else:
            return render(request, 'users/invalid-pwd.html')
    except Exception as e:
        return HttpResponse("You can't do that!")
    return redirect('my-profile')


from datetime import datetime, timedelta


def notifications(request):
    context = {}
    return render(request, 'mobile-notifications.html', context)
