from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import User
# this is still being implemented 

class UserAPITests(APITestCase):
    def setUp(self):
        # Setup run before every test method.
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        self.client.force_authenticate(self.admin_user)  # Simulate logged-in user
        
        self.normal_user = User.objects.create_user('user', 'user@example.com', 'user123', role='Staff')

    def test_create_user(self):
        # Test creating a new user.
        url = reverse('user-list')
        data = {'username': 'newuser', 'email': 'newuser@example.com', 'password': 'newpass123', 'role': 'Staff'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

    def test_get_users(self):
        # Test retrieving a list of users.
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Change 2 to the number of expected users

    def test_delete_user(self):
        # Test deleting a user.
        url = reverse('user-detail', args=[self.normal_user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 1)

    # ... Additional tests for update and partial_update

class UserBusinessLogicTests(TestCase):
    def test_user_role_assignment(self):
        # Test the logic that assigns roles to users.
        user = User.objects.create_user('testuser', 'test@example.com', 'password123')
        user.role = 'Manager'  # Business logic might determine this
        user.save()

        self.assertEqual(user.role, 'Manager')

