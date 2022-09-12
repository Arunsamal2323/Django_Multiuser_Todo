from django.contrib import admin
from account. models import Profile
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("profile_id", "user_id", "user", "view_tasks_link")
    list_filter = ("user",)
    list_display_links=['user']
    search_fields = ("first_name__startswith", )

    def view_tasks_link(self, obj):
        count = obj.user.taskdetails_set.count()
        url = (("admin:MultiuserToDo_task_changelist") + "?" +
               urlencode({"author__id": f"{obj.user.id}"}))
        return format_html('<a href="{}">{} Tasks</a>', url, count)
    view_tasks_link.short_description = "No. of Tasks"


    def user_id(self, obj):
        '''Returns the User ID of the current profile'''
        return obj.user.id
    
    
    def profile_id(self, obj):
        '''Returns the Profile ID of the current profile'''
        return obj.id


# @admin.register(Profile,ProfileAdmin)
admin.site.register(Profile,ProfileAdmin)
                
