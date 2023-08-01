import pytest
from rest_framework import status

from fixtures.user import profile


class TestRegisterView:

    endpoint = '/api/v1/users/register/'

    @pytest.mark.django_db
    def test_register(self, client):
        data = {
            "username": "johndoe",
            "email": "johndoe@yopmail.com",
            "password": "test_password",
            "password2": "test_password",
            "first_name": "John",
            "last_name": "Doe"
        }
        response = client.post(self.endpoint, data)

        assert response.status_code == status.HTTP_201_CREATED


class TestLoginView:

    endpoint = '/api/v1/users/login/'

    @pytest.mark.django_db
    def test_login(self, client, profile):
        data = {
            "username": profile.user.username,
            "password": "test_password" 
        }
        response = client.post(self.endpoint, data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['tokens']['access']
        assert response.data['tokens']['refresh']


class TestLogoutView:

    endpoint = '/api/v1/users/'

    @pytest.mark.django_db
    def test_logout(self, client, profile):
        data_login = {
            "username": profile.user.username,
            "password": "test_password" 
        }
        login_response = client.post(self.endpoint + 'login/', data_login)
        data = {"refresh": login_response.data['tokens']['refresh']}
        access = login_response.data['tokens']['access']
        response = client.post(self.endpoint + 'logout/', data, headers={"Authorization": f"Bearer {access}"})

        assert response.status_code == status.HTTP_205_RESET_CONTENT


class TestUserView:

    endpoint = '/api/v1/users/'

    @pytest.mark.django_db
    def test_get_user(self, client, profile):
        data_login = {
            "username": profile.user.username,
            "password": "test_password" 
        }
        login_response = client.post(self.endpoint + 'login/', data_login)
        access = login_response.data['tokens']['access']
        response = client.get(self.endpoint + 'user/', headers={"Authorization": f"Bearer {access}"})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == profile.user.username

    @pytest.mark.django_db
    def test_update_user(self, client, profile):
        data_login = {
            "username": profile.user.username,
            "password": "test_password" 
        }
        login_response = client.post(self.endpoint + 'login/', data_login)
        access = login_response.data['tokens']['access']
        data = {"username": "new_test_user"}
        response = client.put(self.endpoint + 'user/', data, headers={"Authorization": f"Bearer {access}"})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == data['username']


class TestProfileView:

    endpoint = '/api/v1/users/'

    @pytest.mark.django_db
    def test_get_profile(self, client, profile):
        data_login = {
            "username": profile.user.username,
            "password": "test_password" 
        }
        login_response = client.post(self.endpoint + 'login/', data_login)
        access = login_response.data['tokens']['access']
        response = client.get(self.endpoint + 'profile/', headers={"Authorization": f"Bearer {access}"})

        assert response.status_code == status.HTTP_200_OK
        print(response.data)
        assert response.data['user'] == f"{profile.user.first_name} {profile.user.last_name}"

    @pytest.mark.django_db
    def test_update_profiler(self, client, profile):
        data_login = {
            "username": profile.user.username,
            "password": "test_password" 
        }
        login_response = client.post(self.endpoint + 'login/', data_login)
        access = login_response.data['tokens']['access']
        data = {"username": "new_test_user"}
        response = client.put(self.endpoint + 'profile/', data, headers={"Authorization": f"Bearer {access}"})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['user'] == f"{profile.user.first_name} {profile.user.last_name}"
