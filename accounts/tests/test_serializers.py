import pytest
from accounts.models import User
from accounts.serializers import RegisterSerializer  # your real serializer

@pytest.mark.django_db
def test_email_must_be_unique():
    User.objects.create_user(
        username="user1",
        email="duplicate@example.com",
        password="pass123"
    )

    serializer = RegisterSerializer(data={
        "username": "user2",
        "email": "duplicate@example.com",
        "password": "anotherpass"
    })

    assert not serializer.is_valid()
    assert "email" in serializer.errors
