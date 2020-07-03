from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='profile')
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
    joined_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "@{}".format(self.user.username)
