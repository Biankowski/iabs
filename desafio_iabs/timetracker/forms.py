from django import forms
from .models import Task, TimeEntry

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['description']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descreva a tarefa...'
            })
        }

class TimeEntryForm(forms.ModelForm):
    class Meta:
        model = TimeEntry
        fields = ['task', 'entry_date', 'duration', 'description']
        widgets = {
            'task': forms.Select(attrs={'class': 'form-select'}),
            'entry_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'duration': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'step': '1'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descreva o trabalho realizado...'
            })
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['task'].queryset = Task.objects.filter(user=user)