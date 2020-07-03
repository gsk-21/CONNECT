from itertools import chain
from operator import attrgetter
from posts.models import Post, Comment, Reply, PostLike
from django.db.models import Q
from groups.models import Group, GroupMember
from datetime import datetime, timedelta


def notifications(request):
    context = {}
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    if request.user.is_authenticated:

        name = str(request.user.first_name.split(" ")[0])
        context['name'] = name

        communities = Group.objects.all()
        today_communities = communities.filter(datetime__date=today)
        yesterday_communities = communities.filter(datetime__date=yesterday)
        earlier_communities = communities.filter(~Q(datetime__date=today)).filter(~Q(datetime__date=yesterday))

        likes = PostLike.objects.filter(post__author=request.user)
        likes = likes.filter(~Q(user=request.user))

        today_likes = likes.filter(datetime__date=today)
        yesterday_likes=likes.filter(datetime__date=yesterday)
        earlier_likes = likes.filter(~Q(datetime__date=today)).filter(~Q(datetime__date=yesterday))

        posts = Post.objects.filter(group__members=request.user).order_by('posted_on').reverse()
        posts = posts.filter(~Q(author=request.user))

        today_posts = posts.filter(datetime__date=today)
        yesterday_posts = posts.filter(datetime__date=yesterday)
        earlier_posts = posts.filter(~Q(datetime__date=today)).filter(~Q(datetime__date=yesterday))

        comments = Comment.objects.filter(post__author=request.user).order_by('commented_on').reverse()
        comments = comments.filter(~Q(author=request.user))

        today_comments = comments.filter(datetime__date=today)
        yesterday_comments = comments.filter(datetime__date=yesterday)
        earlier_comments = comments.filter(~Q(datetime__date=today)).filter(~Q(datetime__date=yesterday))

        replies = Reply.objects.filter(reply_to=request.user).order_by('replied_on').reverse()
        replies = replies.filter(~Q(user=request.user))

        today_replies = replies.filter(datetime__date=today)
        yesterday_replies = replies.filter(datetime__date=yesterday)
        earlier_replies = replies.filter(~Q(datetime__date=today)).filter(~Q(datetime__date=yesterday))

        today_notifications = sorted(chain(today_posts, today_comments,today_communities,
                                           today_replies,today_likes),
                                     key=attrgetter('datetime'), reverse=True)

        yesterday_notifications = sorted(chain(yesterday_posts, yesterday_comments,yesterday_communities,
                                               yesterday_likes,yesterday_replies),
                                         key=attrgetter('datetime'), reverse=True)

        earlier_notifications = sorted(chain(earlier_posts, earlier_comments,earlier_communities,
                                             earlier_likes,earlier_replies),
                                       key=attrgetter('datetime'), reverse=True)

        context['today'] = today_notifications
        context['yesterday'] = yesterday_notifications
        context['earlier'] = earlier_notifications

    return context
