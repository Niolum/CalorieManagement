import pytest

from calorie.models import Category, Product


data_category = {
    "name": "test_category",
    "photo": "test/path/test_category.png",
    "slug": "testcategory"
}

@pytest.fixture
def category(db):
    return Category.objects.create(**data_category)


data_product = {
    "name": "test_product",
    "photo": "product/test_category/test_product.png",
    "calorie": "20.00",
    "fat": "10.00",
    "protein": "5.00",
    "carbohydrate": "5.00",
    "slug": "testproduct"
}


@pytest.fixture
def product(db):
    category = Category.objects.create(**data_category)
    data_product["category"] = category
    return Product.objects.create(**data_product)
