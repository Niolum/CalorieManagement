import pytest

from fixtures.user import profile
from fixtures.calorie import product
from cart.models import Cart, CartProduct


@pytest.mark.django_db
def test_create_cart(profile):
    cart = Cart.objects.create(owner=profile)
    assert cart.owner == profile
    assert cart.total_calorie == 0
    assert cart.total_fat == 0
    assert cart.total_protein == 0
    assert cart.total_carbohydrate == 0


@pytest.mark.django_db
def test_create_cart_product(profile, product):
    cart = Cart.objects.create(owner=profile)
    cart_product = CartProduct.objects.create(user=profile, cart=cart, product=product)
    assert cart_product.user == profile
    assert cart_product.cart == cart
    assert cart_product.product == product
    assert cart_product.quantity == 1
    assert cart_product.sum_calorie == product.calorie
    assert cart_product.sum_fat == product.fat
    assert cart_product.sum_protein == product.protein
    assert cart_product.sum_carbohydrate == product.carbohydrate