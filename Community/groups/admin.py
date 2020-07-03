from django.contrib import admin
from .models import Group, GroupMember

from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from .models import Group
from .forms import GroupChangeListForm


# Register your models here.

class GroupAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'created_on']
    fields = ['name', 'description','created_by' ,'group_profile_pic', 'created_on','datetime', 'slug','members' ]
    readonly_fields = ['members']

   # filter_vertical = ('members',)

class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'group']
    search_fields = ['user__username', 'group__name']


admin.site.register(Group, GroupAdmin)
admin.site.register(GroupMember, GroupMemberAdmin)
