import pytest
from rest_framework.test import APIClient
from accounts.models import User

@pytest.mark.django_db
def test_jwt_login_success():
    client = APIClient()

    User.objects.create_user(
        username="loginuser",
        email="login@example.com",
        password="testpass123"
    )

    response = client.post(
        "/api/auth/login/",
        {
            "username": "loginuser",
            "password":"testpass123"
        },
        format="json"
    )

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data
