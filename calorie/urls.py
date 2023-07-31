from django.urls import path

from calorie.views import (
    CategoryListAPIView,
    CategoryAPIView,
    ProductListAPIView,
    ProductAPIView
)


urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='categories'),
    path('categories/<slug:slug>/', CategoryAPIView.as_view(), name='category'),
    path('products/', ProductListAPIView.as_view(), name='products'),
    path('products/<slug:slug>/', ProductAPIView.as_view(), name='product')
]