from rest_framework import viewsets, generics

from rest_framework.exceptions import NotFound
from account.serializers import ProfileSerializer, TaskSerializer
from django.shortcuts import render, redirect
from django.contrib import messages
from django.template import RequestContext
from . forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

from django.contrib.auth.decorators import login_required
from django.http import Http404
from task.models import TaskDetails
from django.contrib.auth.models import User



class ProfileViewSet(generics.ListAPIView):
    serializer_class = ProfileSerializer
    
    def get_queryset(self):
        uname = self.kwargs['username']
        user = User.objects.filter(username=uname).first()
        if user is not None:
            return User.objects.filter(username=user)
        else:
            raise NotFound()



class TaskViewSet(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        uname = self.kwargs['username']
        user = User.objects.filter(username=uname).first()
        # print(f'{user.id}')
        if user is not None:
            return TaskDetails.objects.filter(author=user.id)
        else:
            raise NotFound()


def register(request):
    '''Registration Form'''
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
           
            form.save()
           
            fname = form.cleaned_data.get('first_name')
            
            messages.add_message(
                request, messages.SUCCESS, f"Hey {fname}, Your account has been created successfully. You can login now.")
            
            return redirect('login')

    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form, 'title': 'Register'})


@login_required
def profile(request):

    current_user = request.user
    fname = User.objects.filter(username=current_user).first().first_name
    lname = User.objects.filter(username=current_user).first().last_name
    context = {
        'tasks': current_user.taskdetails_set.all(),
        'active_count': TaskDetails.objects.filter(author=current_user, is_checked=False).count(),
        'completed_count': TaskDetails.objects.filter(author=current_user, is_checked=True).count(),
        'title': current_user,
        'name': fname + ' ' + lname
     }
    return render(request, 'users/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.add_message(request, messages.INFO,
                                 f"Your details have been saved succesfully.")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        # print(dir(request.user.profile))
        p_form = ProfileUpdateForm(instance=request.user.profile)
        context = {
        'u_form': u_form,
        'p_form': p_form,
        'title': 'Edit Profile'
    }

    return render(request, 'users/edit_profile.html', context)
