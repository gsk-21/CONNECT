from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from groups.models import Group
from groups.extras import get_unique_slug
from django.contrib.auth.models import User


# User = get_user_model()

# Create your models here.


class Post(models.Model):
    post_pic = models.ImageField(upload_to='post-pics', blank=True)
    title = models.CharField(max_length=500, blank=False)
    message = models.TextField()
    posted_on = models.DateTimeField(default=timezone.now)
    datetime = models.DateTimeField(default=timezone.now, null=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name='posts', null=True, blank=True, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, through='PostLike', related_name='post_likes')
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, 'title', 'slug')
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-posted_on']


class PostLike(models.Model):
    post = models.ForeignKey(Post, related_name='post_likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_likes', on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('post','user')

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, related_name='authors', on_delete=models.CASCADE, null=True)
    comment = models.TextField()
    commented_on = models.DateTimeField(default=timezone.now)
    datetime = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.comment


class Reply(models.Model):
    comment = models.ForeignKey(Comment, related_name='replies', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    reply = models.TextField()
    replied_on = models.DateTimeField(default=timezone.now)
    reply_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reply_to', null=True)
    reply_for = models.CharField(max_length=10, null=True)
    datetime = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.reply



