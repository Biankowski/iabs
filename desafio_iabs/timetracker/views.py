from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Task, TimeEntry

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