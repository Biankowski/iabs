from django.shortcuts import render
from .models import Task, TimeEntry

def list_tasks(request):
    tasks = Task.objects.select_related('user').all()
    
    return render(request, 'timetracker/task_list.html', {'tasks': tasks})