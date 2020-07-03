from django.contrib import admin
from .models import Post, Comment, Reply,PostLike


# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'group', 'posted_on']
    search_fields = ['group__name', 'author__username']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'comment', 'author', 'commented_on']
    search_fields = ['comment']


class ReplyAdmin(admin.ModelAdmin):
    model = Reply
    list_display = ['reply', 'post', 'comment', 'reply_by', 'replying_to','reply_for']
    search_fields = ['user__first_name', 'reply']

    def post(self, obj):
        return obj.comment.post

    def reply_by(self, obj):
        return obj.user.first_name

    def replying_to(self, obj):
        return obj.reply_to.first_name

class PostLikeAdmin(admin.ModelAdmin):
    model = PostLike
    list_display = ['post','user']


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Reply, ReplyAdmin)
admin.site.register(PostLike,PostLikeAdmin)
