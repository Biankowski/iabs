from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

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

    def __str__(self):
        return self.description

    def clean(self):
        super().clean()
        if self.description and len(self.description.strip()) < 3:
            raise ValidationError('Descrição deve ter pelo menos 3 caracteres')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'

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

    def __str__(self):
        return f"{self.task.description} - {self.duration} em {self.entry_date}"

    def clean(self):
        super().clean()
        
        if self.duration and self.duration.total_seconds() <= 0:
            raise ValidationError('Duration must be positive')
        
        if self.duration and self.duration.total_seconds() > 86400:
            raise ValidationError('Duration cannot exceed 24 hours')
        
        if self.entry_date and self.entry_date > timezone.now().date():
            raise ValidationError('Entry date cannot be in the future')

    class Meta:
        ordering = ['-entry_date', '-created_at']
        verbose_name = 'Registro de Tempo'
        verbose_name_plural = 'Registros de Tempo'
    
