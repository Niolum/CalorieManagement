from rest_framework import serializers

from calorie.models import Product, Category



class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'photo', 'slug']


class CategoryDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'photo', 'slug']


class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'photo', 'slug']


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategoryDetailSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'photo', 'calorie', 'protein', 'fat', 'carbohydrate', 'slug']