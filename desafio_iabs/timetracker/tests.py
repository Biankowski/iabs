from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta, date
from .models import Task, TimeEntry


class TaskModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2', 
            password='testpass123'
        )

    def test_task_creation_with_valid_data(self):
        task = Task.objects.create(
            user=self.user1,
            description='Finalizar a documentação do projeto'
        )
        
        self.assertEqual(task.user, self.user1)
        self.assertEqual(task.description, 'Finalizar a documentação do projeto')
        self.assertIsNotNone(task.created_at)
        self.assertTrue(isinstance(task.created_at, datetime))

    def test_task_str_representation(self):
        task = Task.objects.create(
            user=self.user1,
            description='Testar a tarefa'
        )
        
        self.assertEqual(str(task), 'Testar a tarefa')

    def test_task_user_relationship(self):
        task = Task.objects.create(
            user=self.user1,
            description='Testar a relação entre usuário e tarefa'
        )
        
        self.assertEqual(task.user, self.user1)
        
        self.assertIn(task, self.user1.tasks.all())

    def test_task_description_validation_too_short(self):
        task = Task(
            user=self.user1,
            description='ab'
        )
        
        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_task_description_validation_whitespace_only(self):
        task = Task(
            user=self.user1,
            description='   '
        )
        
        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_task_description_validation_valid_length(self):
        task = Task(
            user=self.user1,
            description='Descrição válida'
        )
        
        try:
            task.full_clean()
        except ValidationError:
            self.fail("ValidationError raised unexpectedly")

    def test_task_ordering(self):
        task1 = Task.objects.create(
            user=self.user1,
            description='Primeira tarefa'
        )
        
        task2 = Task.objects.create(
            user=self.user1,
            description='Segunda tarefa'
        )
        
        tasks = list(Task.objects.all())
        
        self.assertEqual(tasks[0], task2)
        self.assertEqual(tasks[1], task1)

    def test_task_verbose_names(self):
        task = Task()
        
        self.assertEqual(task._meta.verbose_name, 'Tarefa')
        self.assertEqual(task._meta.verbose_name_plural, 'Tarefas')


class TimeEntryModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='testpass123'
        )
        
        self.task1 = Task.objects.create(
            user=self.user1,
            description='Testar a tarefa para registros de tempo'
        )
        self.task2 = Task.objects.create(
            user=self.user2,
            description='Outra tarefa do usuário'
        )

    def test_time_entry_creation_with_valid_data(self):
        entry_date = date.today()
        duration = timedelta(hours=2, minutes=30)
        
        time_entry = TimeEntry.objects.create(
            task=self.task1,
            entry_date=entry_date,
            duration=duration,
            description='Trabalhado na implementação da funcionalidade'
        )
        
        self.assertEqual(time_entry.task, self.task1)
        self.assertEqual(time_entry.entry_date, entry_date)
        self.assertEqual(time_entry.duration, duration)
        self.assertEqual(time_entry.description, 'Trabalhado na implementação da funcionalidade')
        self.assertIsNotNone(time_entry.created_at)

    def test_time_entry_creation_without_description(self):
        time_entry = TimeEntry.objects.create(
            task=self.task1,
            entry_date=date.today(),
            duration=timedelta(hours=1)
        )
        
        self.assertEqual(time_entry.description, '')

    def test_time_entry_str_representation(self):
        entry_date = date(2024, 8, 3)
        duration = timedelta(hours=2, minutes=30)
        
        time_entry = TimeEntry.objects.create(
            task=self.task1,
            entry_date=entry_date,
            duration=duration,
            description='Testar o trabalho'
        )
        
        expected_str = f"{self.task1.description} - {duration} em {entry_date}"
        self.assertEqual(str(time_entry), expected_str)

    def test_time_entry_task_relationship(self):
        time_entry = TimeEntry.objects.create(
            task=self.task1,
            entry_date=date.today(),
            duration=timedelta(hours=1)
        )
        
        self.assertEqual(time_entry.task, self.task1)
        
        self.assertIn(time_entry, self.task1.time_entries.all())

    def test_duration_validation_max_24_hours(self):
        time_entry = TimeEntry(
            task=self.task1,
            entry_date=date.today(),
            duration=timedelta(hours=25)
        )
        
        with self.assertRaises(ValidationError):
            time_entry.full_clean()

    def test_duration_validation_exactly_24_hours(self):
        time_entry = TimeEntry(
            task=self.task1,
            entry_date=date.today(),
            duration=timedelta(hours=24)
        )
        
        try:
            time_entry.full_clean()
        except ValidationError:
            self.fail("ValidationError raised unexpectedly for 24-hour duration")

    def test_entry_date_validation_future_date(self):
        future_date = date.today() + timedelta(days=1)
        
        time_entry = TimeEntry(
            task=self.task1,
            entry_date=future_date,
            duration=timedelta(hours=2)
        )
        
        with self.assertRaises(ValidationError):
            time_entry.full_clean()

    def test_entry_date_validation_today(self):
        time_entry = TimeEntry(
            task=self.task1,
            entry_date=date.today(),
            duration=timedelta(hours=2)
        )
        
        try:
            time_entry.full_clean()
        except ValidationError:
            self.fail("ValidationError raised unexpectedly for today's date")

    def test_entry_date_validation_past_date(self):
        past_date = date.today() - timedelta(days=1)
        
        time_entry = TimeEntry(
            task=self.task1,
            entry_date=past_date,
            duration=timedelta(hours=2)
        )
        
        try:
            time_entry.full_clean()
        except ValidationError:
            self.fail("ValidationError raised unexpectedly for past date")

    def test_time_entry_ordering(self):
        today = date.today()
        yesterday = today - timedelta(days=1)
        
        entry1 = TimeEntry.objects.create(
            task=self.task1,
            entry_date=yesterday,
            duration=timedelta(hours=1)
        )
        
        entry2 = TimeEntry.objects.create(
            task=self.task1,
            entry_date=today,
            duration=timedelta(hours=2)
        )
        
        entries = list(TimeEntry.objects.all())
        
        self.assertEqual(entries[0], entry2)
        self.assertEqual(entries[1], entry1)

    def test_time_entry_verbose_names(self):
        time_entry = TimeEntry()
        
        self.assertEqual(time_entry._meta.verbose_name, 'Registro de Tempo')
        self.assertEqual(time_entry._meta.verbose_name_plural, 'Registros de Tempo')
