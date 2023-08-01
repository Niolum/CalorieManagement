import pytest
from rest_framework import status

from fixtures.user import profile
from fixtures.calorie import product
from cart.models import CartProduct


class TestCartViewSet:

    endpoint = '/api/v1/carts/cart/'
    endpoint_login = '/api/v1/users/'

    def login(self, client, profile):
        data_login = {
                "username": profile.user.username,
                "password": "test_password" 
        }

        login_response = client.post(self.endpoint_login + 'login/', data_login)
        access = login_response.data['tokens']['access']

        return access

    @pytest.mark.django_db
    def test_create(self, client, profile):
        access = self.login(client, profile)
        data = {"owner": profile.id}
        response = client.post(self.endpoint, data, headers={"Authorization": f"Bearer {access}"})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id']
        assert response.data['owner'] == profile.id
        assert response.data['total_calorie'] == '0.00'
        assert response.data['total_fat'] == '0.00'
        assert response.data['total_protein'] == '0.00' 
        assert response.data['total_carbohydrate'] == '0.00'
    
    @pytest.mark.django_db
    def test_retrieve(self, client, profile):
        access = self.login(client, profile)
        response = client.get(self.endpoint + 'current_user_cart/', headers={"Authorization": f"Bearer {access}"})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id']
        assert response.data['owner'] == profile.id
        assert response.data['total_calorie'] == '0.00'
        assert response.data['total_fat'] == '0.00'
        assert response.data['total_protein'] == '0.00' 
        assert response.data['total_carbohydrate'] == '0.00'

    @pytest.mark.django_db
    def test_add_product(self, client, profile, product):
        access = self.login(client, profile)
        response = client.put(self.endpoint + f'current_user_cart/add_to_cart/{product.id}/', headers={"Authorization": f"Bearer {access}"})

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'detail': 'Продукт успешно добавлен в корзину'}

    @pytest.mark.django_db
    def test_change_qty(self, client, profile, product):
        access = self.login(client, profile)
        add_response = client.put(self.endpoint + f'current_user_cart/add_to_cart/{product.id}/', headers={"Authorization": f"Bearer {access}"})
        cart_product = CartProduct.objects.get(product=product)
        response = client.patch(self.endpoint + f'current_user_cart/change_qty/3/{cart_product.id}/', headers={"Authorization": f"Bearer {access}"})

        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_remove_product(self, client, profile, product):
        access = self.login(client, profile)
        add_response = client.put(self.endpoint + f'current_user_cart/add_to_cart/{product.id}/', headers={"Authorization": f"Bearer {access}"})
        cart_product = CartProduct.objects.get(product=product)
        response = client.put(self.endpoint + f'current_user_cart/remove_from_cart/{cart_product.id}/', headers={"Authorization": f"Bearer {access}"})

        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_remove_all_products(self, client, profile, product):
        access = self.login(client, profile)
        add_response = client.put(self.endpoint + f'current_user_cart/add_to_cart/{product.id}/', headers={"Authorization": f"Bearer {access}"})
        response = client.put(self.endpoint + f'current_user_cart/remove_all_from_cart/', headers={"Authorization": f"Bearer {access}"})

        assert response.status_code == status.HTTP_200_OK