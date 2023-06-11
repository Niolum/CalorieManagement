from rest_framework import serializers

from cart.models import CartProduct, Cart
from calorie.serializers import ProductListSerializer
from user.serializers import ProfileSerializer



class CartProductSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()

    class Meta:
        model = CartProduct
        fields = ['id', 'product', 'quantity', 'sum_calorie', 'sum_fat', 'sum_protein', 'sum_carbohydrate']


class CartSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer()
    cart_products = CartProductSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'owner', 'cart_products', 'total_calorie', 'total_fat', 'total_protein', 'total_carbohydrate']