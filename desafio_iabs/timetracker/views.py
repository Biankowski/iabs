from .models import Task, TimeEntry
from .forms import TaskForm, TimeEntryForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Conta criada para {username}!')
            login(request, user)
            return redirect('list_tasks')
    else:
        form = UserCreationForm()
    return render(request, 'timetracker/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('list_tasks')
        else:
            messages.error(request, 'Nome de usuário ou senha inválidos.')
    return render(request, 'timetracker/login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('login')

@login_required
def list_tasks(request):
    tasks = Task.objects.filter(user=request.user).select_related('user')
    
    return render(request, 'timetracker/task_list.html', {'tasks': tasks})

@login_required
def list_time_entries(request):
    time_entries = TimeEntry.objects.filter(task__user=request.user).select_related('task', 'task__user')
    
    task_filter = request.GET.get('task')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    description_filter = request.GET.get('description')
    
    if task_filter:
        time_entries = time_entries.filter(task__id=task_filter)
    
    if date_from:
        time_entries = time_entries.filter(entry_date__gte=date_from)
    
    if date_to:
        time_entries = time_entries.filter(entry_date__lte=date_to)
    
    if description_filter:
        time_entries = time_entries.filter(description__icontains=description_filter)
    
    user_tasks = Task.objects.filter(user=request.user)
    
    context = {
        'time_entries': time_entries,
        'user_tasks': user_tasks,
        'filters': {
            'task': task_filter,
            'date_from': date_from,
            'date_to': date_to,
            'description': description_filter,
        }
    }
    
    return render(request, 'timetracker/time_entry_list.html', context)

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Tarefa criada com sucesso!')
            return redirect('list_tasks')
    else:
        form = TaskForm()
    
    return render(request, 'timetracker/create_task.html', {'form': form})

@login_required
def create_time_entry(request):
    if request.method == 'POST':
        form = TimeEntryForm(request.user, request.POST)
        if form.is_valid():
            time_entry = form.save()
            messages.success(request, 'Registro de tempo criado com sucesso!')
            return redirect('list_time_entries')
    else:
        initial_data = {}
        task_id = request.GET.get('task')
        if task_id and Task.objects.filter(id=task_id, user=request.user).exists():
            initial_data['task'] = task_id
        
        form = TimeEntryForm(request.user, initial=initial_data)
    
    return render(request, 'timetracker/create_time_entry.html', {'form': form})