from django.urls import path, include
from rest_framework.routers import SimpleRouter

from cart.views import CartViewSet



router_cart = SimpleRouter()
router_cart.register('cart', CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router_cart.urls))
]