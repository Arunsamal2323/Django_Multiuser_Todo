from django.urls import reverse
from django.contrib import admin
from django.utils.http import urlencode
from task.models import TaskDetails


@admin.register(TaskDetails)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "task_title", "is_checked")
    list_filter = ("author",) 
    list_display_links=['task_title']


    