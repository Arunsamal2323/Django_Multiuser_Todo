from rest_framework import serializers
from django.contrib.auth.models import User
from task.models import TaskDetails
from account.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('username', 'email')


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = TaskDetails
        fields = ('task_title', 'is_checked', 'date_posted')