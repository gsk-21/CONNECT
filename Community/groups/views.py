from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import (DetailView, ListView, DeleteView)
from .models import Group, GroupMember
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import get_user_model


# User = get_user_model()


# Create your views here.
@login_required
def create_community(request):
    if request.method == 'POST':
        name = request.POST.get('group-name')
        desc = request.POST.get('description')

        group = Group()
        group.name = name
        group.description = desc
        group.created_by = request.user
        if 'group_profile_pic' in request.FILES:
            group.group_profile_pic = request.FILES['group_profile_pic']
            print(request.FILES['group_profile_pic'])
        group.save()
        group.members.add(request.user)

        return redirect('home')
    else:
        return render(request, 'groups/create-community.html')


@login_required
def join_community(request, slug):
    membership = GroupMember()
    user = request.user
    try:
        group = Group.objects.get(slug=slug)

        if user not in Group.objects.all():
            membership.user = user
            membership.group = group
            membership.save()
            return redirect('community-detail', slug=slug)

        else:
            return HttpResponse("Already a member!")

    except:
        return HttpResponse('<center><h4>ALREADY A MEMBER!</h4></center>')


@login_required
def exit_community(request, slug):
    group = Group.objects.get(slug=slug)
    user = request.user
    try:
        membership = GroupMember.objects.get(user=user, group=group)
        membership.delete()
        return redirect('community-detail', slug=slug)
        # return redirect(request, 'community-detail', slug=group.slug)
    except:
        return HttpResponse('<center><br><br><br><br><h4>NOT A MEMBER!</h4></center>')


class CommunityList(ListView):
    # login_url = '/login/'
    # redirect_field_name = 'groups/community-list.html'
    model = Group
    template_name = 'groups/community-list.html'
    context_object_name = 'communities'

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:

            context = super(CommunityList, self).get_context_data(**kwargs)
            context['following_communities'] = GroupMember.objects.filter(user=self.request.user)
            context['non_following_communities'] = Group.objects.filter(~Q(members=self.request.user))
            return context
        else:
            context = super(CommunityList, self).get_context_data(**kwargs)
            context['communities'] = Group.objects.all()
            return context


class CommunityDetail(LoginRequiredMixin,DetailView):
    login_url = '/login/'
    redirect_field_name = 'groups/community-list.html'
    model = Group
    template_name = 'groups/community-detail.html'
    context_object_name = 'community'


class MyCommunityList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'groups/my-community-list.html'
    model = Group
    template_name = 'groups/my-community-list.html'
    context_object_name = 'my_communities'

    def get_queryset(self):
        queryset = self.model.objects.filter(created_by=self.request.user)
        return queryset


class DeleteCommunity(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'index.html'
    model = Group
    template_name = 'groups/delete-community.html'
    context_object_name = 'community'
    success_url = '/'

    def get_queryset(self):
        return self.model.objects.filter(created_by=self.request.user)


class FollowingCommunityList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'groups/following-community-list.html'
    model = GroupMember
    template_name = 'groups/following-community-list.html'
    context_object_name = 'following_communities'

    def get_queryset(self):
        queryset = self.model.objects.filter(user=self.request.user)
        return queryset


def user_following_community(request, pk):
    user = User.objects.get(pk=pk)
    context = {}
    context['following_communities'] = GroupMember.objects.filter(user=user)
    context['about_user'] = user
    return render(request, 'groups/user-following-community.html', context)


def user_created_community(request, pk):
    user = User.objects.get(pk=pk)
    context = {}
    context['created_communities'] = Group.objects.filter(created_by=user)
    context['about_user'] = user
    return render(request, 'groups/user-created-community.html', context)


def update_community_pic(request):
    if request.method == 'POST':
        group = Group.objects.get(slug=request.POST.get('community-slug'))
        group.group_profile_pic = request.FILES['new-community-profile-pic']
        group.save()

    return redirect('community-detail', slug=request.POST.get('community-slug'))


def remove_community_profile_pic(request, slug):
    group = Group.objects.get(slug=slug)
    if group.group_profile_pic:
        group.group_profile_pic.delete(save=True)

    return redirect('community-detail', slug=slug)
