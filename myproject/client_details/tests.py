from django.test import TestCase
# this is still being implemented 
# client_details/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Client

class ClientAPITests(TestCase):
    def setUp(self):
        # Set up any initial data or state for the tests
        self.client = APIClient()
        self.test_client = Client.objects.create(
            org_name="Test Org",
            project_name="Test Project",
            description="Test Description",
            estimation=100.0
        )

    def test_create_client(self):
        # Test creating a new client
        url = reverse('client-list')
        data = {
            'org_name': 'New Org',
            'project_name': 'New Project',
            'description': 'New Description',
            'estimation': 200.0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_client(self):
        # Test retrieving a client's details
        url = reverse('client-detail', args=[self.test_client.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_client(self):
        # Test updating a client's details
        url = reverse('client-detail', args=[self.test_client.id])
        data = {
            'org_name': 'Updated Org',
            'project_name': 'Updated Project'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_client(self):
        # Test deleting a client
        url = reverse('client-detail', args=[self.test_client.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
