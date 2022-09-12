from django.shortcuts import render
from task.models import TaskDetails
from django.db.models import Max
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def index(request):
    
    '''The first page of Application.'''
    return render(request, 'MultiuserToDo/index.html')



@csrf_exempt
def tasks(request):
    current_user = request.user
    # print(dir(current_user))
    max_date = current_user.taskdetails_set.all().aggregate(
        max_date=Max('date_posted'))['max_date']
    context = {
        'tasks': current_user.taskdetails_set.all(),
        'max_date': max_date
    }
    return render(request, 'MultiuserToDo/tasks.html', context)



decorators = [csrf_exempt, login_required]


@method_decorator(decorators, name='dispatch')
class TaskListView(ListView):
    ''' Using Class based view - ListView '''
    model = TaskDetails
    template_name = 'MultiuserToDo/tasks.html'  
    context_object_name = 'tasks'

    def get_queryset(self):
        '''Returns the tasks of the currently logged in User'''
        current_user = self.request.user
        return current_user.taskdetails_set.all()


def test(request):
    return render(request, 'MultiuserToDo/test.html')






@csrf_exempt
@login_required
def move_tasks(request):
    ''' Function to move the tasks from Active Table to Complete Table and vice-versa. '''
    if request.method == 'POST':
        task_id = request.POST['task_id']
        task_class = request.POST['task_class']
        if 'mark_as_done' in task_class:
            done_task = TaskDetails.objects.get(pk=task_id)
            done_task.is_checked = True
            done_task.save()
        elif 'mark_as_undone' in task_class:
            undone_task = Task.objects.get(pk=task_id)
            undone_task.is_checked = False
            undone_task.save()
        return HttpResponse("Success!")
    else:
        return HttpResponse("Request method is not GET.")


@csrf_exempt
@login_required
def add_new_task(request):
    # import pdb; pdb.set_trace()
    print('hello')
    '''Adds a New Task to the Task Table in Database.'''
    if request.method == 'POST':
        task_name = request.POST['task_title'].strip()
        creator = request.user
        temp_task = TaskDetails(task_title=task_name, author=creator)
        temp_task.save()
        task_json_string = model_to_dict(
            temp_task, fields=['id', 'task_title', 'author'])

       
        return JsonResponse(task_json_string)

    else:
        return HttpResponse("Request method is not GET.")




@csrf_exempt
@login_required
def delete_task(request):
    '''Deletes a task from the Task Table.'''
    if request.method == 'POST':
        task_id = request.POST['task_id']
        del_task = TaskDetails.objects.get(id=task_id)
        del_task.delete()
        print(f'Deleted the Task with ID: {task_id}')
        return HttpResponse("Deleted the Task")
    else:
        return HttpResponse("Request method is not POST.")


@csrf_exempt
@login_required
def delete_all_completed_tasks(request):
    '''Deletes all the Completed tasks from the Completed Table'''
    if request.method == 'POST':
        del_tasks = TaskDetails.objects.filter(is_checked=1)
        del_tasks.delete()
        return HttpResponse("Successfully Deleted all Completed Tasks")
    else:
        return HttpResponse("Request is not POST.")


@csrf_exempt
@login_required
def update_task(request):
    '''Updates the task'''
    if request.method == 'POST':
        task_id = request.POST['task_id']
        new_task = request.POST['task_name']
        changed_task = TaskDetails.objects.get(id=task_id)
        changed_task.task_title = new_task.strip()
        changed_task.save()
        print(f'Task Updated ID: {task_id}')
        return HttpResponse("Successfully Updated Tasks")
    else:
        return HttpResponse('Request is not POST.')


@csrf_exempt
@login_required
def refresh_data(request):
    '''Returns the updated data after every AJAX Call.'''
    if request.method == 'POST':
        user = request.user
        data = serializers.serialize("json", user.taskdetails_set.all())
        return JsonResponse(data, safe=False)
    else:
        return HttpResponse('Request Method is not POST.')
