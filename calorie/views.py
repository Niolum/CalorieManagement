from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from calorie.models import Product, Category
from calorie.serializers import (
    ProductListSerializer, 
    ProductDetailSerializer, 
    CategoryListSerializer, 
    CategoryDetailSerializer
)
from calorie.pagination import CategoryAPIListPagination, ProductAPIListPagination



class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    permission_classes = [AllowAny]
    pagination_class = CategoryAPIListPagination


class CategoryAPIView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]
    pagination_class = ProductAPIListPagination


class ProductAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'