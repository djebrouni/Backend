import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
import json

@pytest.fixture
def create_user():
    """Fixture to create a user"""
    User = get_user_model()
    return User.objects.create_user(email="test@example.com", password="password123")

@pytest.mark.django_db
def test_signin_valid(create_user, client):
    """Test sign-in with valid credentials"""
    url = reverse('signin')  # Replace with the actual URL name for the sign-in view

    # Request body
    data = {
        'role': 'doctor',
        'email': 'test@example.com',
        'password': 'password123'
    }

    response = client.post(url, json.dumps(data), content_type='application/json')

    assert response.status_code == status.HTTP_200_OK
    assert 'token' in response.json()  # Ensure the token is in the response
