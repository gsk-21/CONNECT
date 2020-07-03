from django.contrib import admin
from django.contrib.auth.models import User
from . import models




# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    model = models.Profile
    list_display = ['user', 'name', 'email',]
    search_fields = ['user__username','user__email']
    readonly_fields =  ['first_name','last_name','email','joined_on',]

    def user(self,obj):
        return obj.user.username
    user.short_description = 'Username'

    def name(self, obj):
        return obj.user.first_name + " " + obj.user.last_name
    name.admin_order_field = 'user'  # Allows column order sorting
    name.short_description = 'Name'  # Renames column head

    def first_name(self,obj):
        return obj.user.first_name

    def last_name(self,obj):
        return obj.user.last_name

    def email(self, obj):
        return obj.user.email

admin.site.register(models.Profile, ProfileAdmin)

