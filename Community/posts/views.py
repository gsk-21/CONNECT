import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse

from django.contrib.auth.models import User
from .models import Post, Comment, Reply, PostLike
from groups.models import Group
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import generic


# Create your views here.
@login_required
def create_post(request):
    # slug = request.GET['slug']
    if request.method == 'POST':
        group_slug = request.POST.get('group-slug')
        post = Post()
        group = Group.objects.get(slug=group_slug)
        post.group = group

        post.title = request.POST.get('post-title')
        post.message = request.POST.get('post-message')
        post.author = request.user

        if 'post_pic' in request.FILES:
            post.post_pic = request.FILES['post_pic']
        post.save()
        return redirect('community-detail', slug=group_slug)
        # return redirect('community-detail', slug=slug)

    else:
        group_slug = request.GET['slug']
        group_name = Group.objects.get(slug=group_slug)
        return render(request, 'posts/create-post.html', {'group_slug': group_slug, 'group_name': group_name})


class AllPosts(generic.ListView):
    model = Post
    context_object_name = 'all_posts'
    template_name = 'posts/all-posts.html'


class MyPosts(LoginRequiredMixin, generic.ListView):
    model = Post
    context_object_name = 'my_posts'
    template_name = 'posts/my-posts.html'

    def get_queryset(self):
        # obj = Post.objects.filter(author = self.request.user)
        queryset = self.model.objects.filter(author=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(MyPosts, self).get_context_data(**kwargs)
        queryset = self.model.objects.filter(author=self.request.user)
        queryset = queryset.filter(group__members = self.request.user)
        queryset = Group.objects.filter(posts__author = self.request.user).distinct()
        #queryset = set(queryset)
        context['posts_communities'] = queryset
        return context


# class PostDetail(LoginRequiredMixin,generic.DeleteView,):
#     login_url = 'login'
#     model = Post
#     template_name = 'posts/post-detail.html'
#     context_object_name = 'post'
#
#     def get_context_data(self, **kwargs):
#         context = super(PostDetail, self).get_context_data(**kwargs)
#         queryset = self.model.objects.filter(author=self.object.author).exclude(slug=self.kwargs['slug'])
#         context['user_posts'] = queryset
#         return context

@login_required
def post_detail(request,slug):
    post = Post.objects.get(slug = slug)

    context = {}
    context['post'] = post
    queryset = Post.objects.filter(author=post.author).exclude(slug=slug)
    context['user_posts'] = queryset
    member = request.user in post.group.members.all()
    if member:
        return render(request,'posts/post-detail.html',context)
    else:
        group_name = str(post.group.name)
        return render(request,'posts/warning.html',{'post':post})





@login_required
def delete_post(request):
    post_to_delete = Post.objects.get(slug=request.POST.get('post_slug'))
    post_to_delete.delete()

    return HttpResponse(
        json.dumps(
            {
                'result': 'Post deleted Successfully'
            }
        ),
        content_type="application/json"
    )


@login_required
def add_comment(request):
    post = Post.objects.get(slug=request.POST.get('post_slug'))
    member = request.user in post.group.members.all()
    comment = Comment()
    comment.comment = request.POST.get('comment_message')
    comment.author = request.user
    comment.post = Post.objects.get(slug=request.POST.get('post_slug'))
    comment.save()

    if member:

        return HttpResponse(
            json.dumps(
                {
                    'result': 'Commented Successfully'
                }
            ),
            content_type="application/json"
        )
    else:
        return HttpResponse('<center style="font-size:2.5rem;"><br><br>'
                            "<br><br><b>LOL! NICE TRY !</b></center>")


@login_required
def delete_comment(request):
    comment_to_delete = Comment.objects.get(pk=request.POST.get('comment_pk'))
    comment_to_delete.delete()

    return HttpResponse(
        json.dumps(
            {
                'result': 'Commented deleted Successfully'
            }
        ),
        content_type="application/json"
    )


@login_required
def reply_comment(request):
    login_url = '/login/'
    redirect_field_name = 'users/user-profile.html'

    comment = Comment.objects.get(pk=request.POST.get('comment_pk'))
    member = request.user in comment.post.group.members.all()

    reply = Reply()
    reply.user = request.user
    reply.reply = request.POST.get('reply_message')
    reply.comment = Comment.objects.get(pk=request.POST.get('comment_pk'))
    reply.reply_for = request.POST.get('reply_for')
    reply.reply_to = User.objects.get(pk=request.POST.get('reply_to_pk'))

    reply.save()
    if member:

        return HttpResponse(
            json.dumps(
                {
                    'result': 'Replied Successfully'
                }
            ),
            content_type="application/json"
        )
    else:
        return HttpResponse('<center style="font-size:2.5rem;"><br>'
                            "<br><br><b>NO WAY YOU DOING THAT </b></center>")



@login_required
def delete_reply(request):
    reply_to_delete = Reply.objects.get(pk=request.POST.get('reply_pk'))
    reply_to_delete.delete()

    return HttpResponse(
        json.dumps(
            {
                'result': 'Reply deleted Successfully'
            }
        ),
        content_type="application/json"
    )


@login_required
def like_toggle(request):
    user = request.user
    if request.method == 'POST':
        post_slug = request.POST['post_slug']
        post = Post.objects.get(slug=post_slug)
        liked = user in post.likes.all()
        if liked:
            like = 0
            post.likes.remove(user)
        else:
            like = 1
            post.likes.add(user)
        liked_by_user = user in post.likes.all()
        likes_count = len(post.likes.all())
        return JsonResponse(
            {'like': like,
             'likes_count':likes_count,
             'liked_by_user':liked_by_user
             }
        )
