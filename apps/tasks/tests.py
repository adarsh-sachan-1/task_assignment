from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from apps.tasks.models import Task
from rest_framework_simplejwt.tokens import RefreshToken


class TaskViewSetTest(APITestCase):

    def setUp(self):
        # Create a superuser (admin) for testing the permissions
        self.admin_user = User.objects.create_superuser(username='adminuser', password='adminpass')
        # Create a regular user for testing without admin permissions
        self.regular_user = User.objects.create_user(username='regularuser', password='regularpass')

        # Generate JWT token for authentication
        self.admin_token = RefreshToken.for_user(self.admin_user).access_token
        self.regular_token = RefreshToken.for_user(self.regular_user).access_token

        self.task_data = {
            'task_name': 'Test Task',
            'description': 'Test Description',
            'due_date': '2024-12-31',
            'status': 'pending',
        }

    def test_create_task_as_admin(self):
        # Authenticate with admin token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')

        response = self.client.post('/v1/tasks/', self.task_data)

        # Check if task is created successfully
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['task_name'], 'Test Task')

    def test_create_task_as_regular_user(self):
        # Authenticate with regular user token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.regular_token}')

        response = self.client.post('/v1/tasks/', self.task_data)

        # Check if the user is unauthorized
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_tasks(self):
        # Authenticate with admin token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')

        # Create a task for the admin user
        Task.objects.create(user=self.admin_user, **self.task_data)

        response = self.client.get('/v1/tasks/')

        # Check if tasks are listed
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_mark_task_as_inactive(self):
        # Authenticate with admin token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')

        # Create a task for the admin user
        task = Task.objects.create(user=self.admin_user, **self.task_data)

        # Mark task as inactive (soft delete)
        response = self.client.delete(f'/v1/tasks/{task.id}/')

        # Check if task status is marked as inactive
        task.refresh_from_db()
        self.assertEqual(task.is_active, False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'Task marked as inactive')

    def test_search_tasks(self):
        # Authenticate with admin token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')

        # Create a task for the admin user
        Task.objects.create(user=self.admin_user, **self.task_data)

        response = self.client.get('/v1/tasks/?search=Test')

        # Check if the task is found
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
        self.assertEqual(response.data['results'][0]['task_name'], 'Test Task')

    def test_ordering_tasks(self):
        # Authenticate with admin token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')

        # Create multiple tasks with different due dates
        Task.objects.create(user=self.admin_user, task_name='Task 1', due_date='2024-11-30', status='pending')
        Task.objects.create(user=self.admin_user, task_name='Task 2', due_date='2024-12-01', status='completed')

        response = self.client.get('/v1/tasks/?ordering=due_date')

        # Check if tasks are ordered correctly by due_date
        self.assertEqual(response.status_code, status.HTTP_200_OK)


