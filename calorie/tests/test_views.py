import pytest
from rest_framework import status

from fixtures.calorie import product, category


class TestCategoryListAPIView:

    endpoint = '/api/v1/calories/categories/'

    @pytest.mark.django_db
    def test_list(self, client, category):
        response = client.get(self.endpoint)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['id'] == category.id
        assert response.data['results'][0]['name'] == category.name
        assert response.data['results'][0]['photo'] == f'http://testserver/media/{category.photo}'
        assert response.data['results'][0]['slug'] == category.slug


class TestCategoryAPIView:

    endpoint = '/api/v1/calories/categories/'

    @pytest.mark.django_db
    def test_retrieve(self, client, category):
        response = client.get(self.endpoint + f'{category.slug}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == category.id
        assert response.data['name'] == category.name
        assert response.data['photo'] == f'http://testserver/media/{category.photo}'
        assert response.data['slug'] == category.slug


class TestProductListAPIView:

    endpoint = '/api/v1/calories/products/'

    @pytest.mark.django_db
    def test_list(self, client, product):
        response = client.get(self.endpoint)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['id'] == product.id
        assert response.data['results'][0]['name'] == product.name
        assert response.data['results'][0]['photo'] == f'http://testserver/media/{product.photo}'
        assert response.data['results'][0]['slug'] == product.slug


class TestProductAPIView:

    endpoint = '/api/v1/calories/products/'

    @pytest.mark.django_db
    def test_retrieve(self, client, product):
        response = client.get(self.endpoint + f'{product.slug}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == product.id
        assert response.data['name'] == product.name
        assert response.data['photo'] == f'http://testserver/media/{product.photo}'
        assert response.data['slug'] == product.slug
        assert response.data['calorie'] == product.calorie
        assert response.data['fat'] == product.fat
        assert response.data['protein'] == product.protein
        assert response.data['carbohydrate'] == product.carbohydrate