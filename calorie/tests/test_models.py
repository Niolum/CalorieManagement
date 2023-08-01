import pytest

from calorie.models import Category, Product


data_category = {
    "name": "test_category",
    "photo": "test/path/test_category.png",
    "slug": "testcategory"
}


@pytest.mark.django_db
def test_create_category():
    category = Category.objects.create(**data_category)
    assert category.name == data_category["name"]
    assert category.photo == data_category["photo"]
    assert category.slug == data_category["slug"]


data_product = {
    "name": "test_product",
    "photo": "product/test_category/test_product.png",
    "calorie": "20.00",
    "fat": "10.00",
    "protein": "5.00",
    "carbohydrate": "5.00",
    "slug": "testproduct"
}


@pytest.mark.django_db
def test_create_product():
    category = Category.objects.create(**data_category)
    data_product["category"] = category
    product = Product.objects.create(**data_product)
    assert product.name == data_product["name"]
    assert product.photo == data_product["photo"]
    assert product.calorie == data_product["calorie"]
    assert product.fat == data_product["fat"]
    assert product.protein == data_product["protein"]
    assert product.carbohydrate == data_product["carbohydrate"]
    assert product.category == category
    assert product.slug == data_product["slug"]