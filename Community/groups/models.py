from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from .extras import get_unique_slug
from django import template

register = template.Library()

# Create your models here.

User = get_user_model()


class Group(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=False, default='')
    group_profile_pic = models.ImageField(upload_to='group-profile-pics', blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(allow_unicode=True, unique=True)
    members = models.ManyToManyField(User, through='GroupMember', related_name='group_member')
    created_by = models.ForeignKey(User,related_name='created_by',on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, 'name', 'slug')
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-datetime']


class GroupMember(models.Model):
    group = models.ForeignKey(Group, related_name='memberships', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_groups', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username



    class Meta:
        unique_together = ('group', 'user')
