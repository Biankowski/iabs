from django.db import models
from django.contrib.auth.models import get_user_model

User = get_user_model()

class Task(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name='Usuário'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )

    description = models.TextField(
        verbose_name='Descrição'
    )

class TimeEntry(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='time_entries',
        verbose_name='Tarefa'
    )

    entry_date = models.DateField(
        verbose_name='Data de entrada'
    )

    duration = models.DurationField(
        verbose_name='Duração'
    )

    description = models.TextField(
        blank=True,
        verbose_name='Descrição'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )
    
