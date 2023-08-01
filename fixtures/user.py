import pytest

from user.models import User, Profile


data_user = {
    "username": "test_user",
    "email": "test@gmail.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "test_password"
}


@pytest.fixture
def profile(db) -> Profile:
    user = User.objects.create_user(**data_user)
    return Profile.objects.get(user=user)