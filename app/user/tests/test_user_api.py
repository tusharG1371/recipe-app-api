"""
Tests for the user api.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_user(**params):
    """create and return a new user."""
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()
    
    def test_create_user_success(self):
        """Test createing a user is successfull."""
        payload = {
            'email':'test@example.com',
            'password':'testpass123',
            'name':'Test Name'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if user with emails exists"""
        payload = {
            'email':'test@example.com',
            'password':'testpass123',
            'name':'Test Name'
        }
        create_user(**payload)
        # Retry to create same user
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is return if password length less than 5 chars"""
        payload = {
            'email':'test@example.com',
            'password':'pass',
            'name':'Test Name'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test generates token for valid credetials"""
        user_details = {
            "email":"test@example.com",
            "password":"testpass123",
            "name":"Test User"
        }
        create_user(**user_details)
        payload = {
            'email':user_details['email'],
            'password':user_details['password']
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid."""
        create_user(email='test@example.com', password='goodPass123')
        payload = {
            "email":"test@example.com",
            "password":"badPass123",
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error."""
        create_user(email='test@example.com', password='goodPass123')
        payload = {
            "email":"test@example.com",
            "password":"",
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)




    