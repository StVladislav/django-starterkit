from rest_framework.test import APITestCase
from django.urls import reverse

from src.authentication.models import User


class UserAuthTests(APITestCase):
    """
    An example how to use tests for djoser login and createuser API.
    
    For local running use: 
    
    >>> python manage.py test authentication

    P.S. If you perform it on a Windows machine and encounter the error related to path 
    set this in opened terminal:

    >>> $env:PYTHONPATH="src"  

    OR for local docker

    >>> docker compose -f docker-compose.dev.yml exec gunicorn python manage.py test authentication
    """
    def setUp(self):
        self.register_url = reverse('user-list')
        self.login_url = reverse('login')

    def test_user_registration(self):
        data = {
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "strongpassword123",
            "re_password": "strongpassword123"
        }
        response = self.client.post(self.register_url, data, format='json')
        user = User.objects.filter(email="testuser@example.com").first()
        self.assertEqual(response.status_code, 201)
        self.assertTrue(user is not None)

    def test_user_login(self):
        User.objects.create_user(
            email="loginuser@example.com",
            first_name="Login",
            last_name="User",
            password="loginpassword123"
        )
        data = {
            "email": "loginuser@example.com",
            "password": "loginpassword123"
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('auth_token', response.data)
