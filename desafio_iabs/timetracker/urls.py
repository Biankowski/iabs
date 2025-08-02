from django.urls import path
from .views import list_tasks

urlpatterns = [
    path('tasks/', list_tasks, name='list_tasks'),
]