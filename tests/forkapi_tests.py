import os
import uuid

import pytest
from authentication.models import User
from recipe.models import Category
from dotenv import load_dotenv
from rest_framework.test import APIClient


load_dotenv()


@pytest.fixture(scope="session")
def api_client():
    client = APIClient()
    client.credentials(HTTP_X_AUTH_HEADER=os.getenv('X_AUTH_HEADER'))

    return client


@pytest.mark.django_db
def test_create_admin_user(api_client):

    admin_user_data = {
        "username": "admin",
        "password": "test123",
        "is_superuser": True
    }
    response = api_client.post("/api/auth/signup", admin_user_data, format="json")
    assert response.status_code == 201

    admin_user = User.objects.get(username=admin_user_data['username'])

    assert admin_user.username == admin_user_data['username']
    assert admin_user.is_superuser == True


@pytest.mark.django_db
def test_create_category(api_client):
    category_data = {
        "name": f"Category-{uuid.uuid4()}"
    }

    response = api_client.post("/api/recipe/category/add", category_data, format="json")
    assert response.status_code == 201

    category = Category.objects.get(name=category_data['name'])

    assert category.name == category_data['name']
    return category
