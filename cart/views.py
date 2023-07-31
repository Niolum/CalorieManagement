from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from cart.serializers import CartProductSerializer, CartSerializer
from cart.models import Cart, CartProduct
from user.models import Profile
from calorie.models import Product



class CartViewSet(ModelViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    def create(self, request, *args, **kwargs):
        cart = Cart.objects.filter(owner=request.data["owner"]).first()
        if cart:
            data = {'detail': 'У данного пользователя уже есть корзина'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return super(CartViewSet, self).create(request, *args, **kwargs)

    @staticmethod
    def get_cart(user):
        if user.is_authenticated:
            profile = get_object_or_404(Profile, pk=user.profile.pk)
            cart, created = Cart.objects.get_or_create(owner=profile)
            return cart
        raise NotAuthenticated

    @staticmethod
    def _get_or_create_cart_product(profile: Profile, cart: Cart, product: Product):
        cart_product, created = CartProduct.objects.get_or_create(
            user=profile,
            product=product,
            cart=cart
        )
        return cart_product, created
    
    @action(methods=['get'], detail=False)
    def current_user_cart(self, *args, **kwargs):
        try:
            cart = self.get_cart(self.request.user)
            cart_serializer = CartSerializer(cart)
            return Response(cart_serializer.data)
        except NotAuthenticated:
            data = {'error': 'Not Authorized'}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        
    @action(methods=['put'], detail=False, url_path='current_user_cart/add_to_cart/(?P<product_id>\d+)')
    def product_add_to_cart(self, *args, **kwargs):
        cart = self.get_cart(user=self.request.user)
        product = get_object_or_404(Product, id=kwargs['product_id'])
        cart_product, created = self._get_or_create_cart_product(self.request.user.profile, cart, product)
        if created:
            cart.cart_products.add(cart_product)
            cart.save()
            data = {'detail': 'Продукт успешно добавлен в корзину'}
            return Response(data, status=status.HTTP_200_OK)
        data = {'detail': 'Продукт уже в корзине'}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['patch'], detail=False, url_path='current_user_cart/change_qty/(?P<qty>\d+)/(?P<cart_product_id>\d+)')
    def product_change_qty(self, *args, **kwargs):
        cart_product = get_object_or_404(CartProduct, id=kwargs['cart_product_id'])
        cart_product.quantity = int(kwargs['qty'])
        cart_product.save()
        cart_product.cart.save()
        return Response(status=status.HTTP_200_OK)
    
    @action(methods=['put'], detail=False, url_path='current_user_cart/remove_from_cart/(?P<cproduct_id>\d+)')
    def product_remove_from_cart(self, *args, **kwargs):
        cart = self.get_cart(user=self.request.user)
        cproduct = get_object_or_404(CartProduct, id=kwargs['cproduct_id'])
        cart.cart_products.remove(cproduct)
        cproduct.delete()
        cart.save()
        return Response(status=status.HTTP_200_OK)
    
    @action(methods=['put'], detail=False, url_path='current_user_cart/remove_all_from_cart')
    def remove_all_product_from_cart(self, *args, **kwargs):
        cart = self.get_cart(user=self.request.user)
        cart.cart_products.clear()
        cart.save()
        return Response(status=status.HTTP_200_OK)