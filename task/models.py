from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User



class TaskDetails(models.Model):
    task_title = models.CharField(max_length=60)
    is_checked = models.BooleanField(default=False)
    date_posted = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.task_title

    class Meta:
        ordering = ('-date_posted',)
