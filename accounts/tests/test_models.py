import pytest
from accounts.models import User

@pytest.mark.django_db
def test_create_user_with_email_and_password():
    user = User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="strongpass123"
    )

    assert user.email == "test@example.com"
    assert user.check_password("strongpass123")
