from django.db import models

from user.models import Profile
from calorie.models import Product



class CartProduct(models.Model):
    user = models.ForeignKey(Profile, verbose_name='Пользователь', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Выбранный продукт', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество', default=1)
    sum_calorie = models.DecimalField(verbose_name='Сумма ккал', default=0, null=True, decimal_places=2, max_digits=20)
    sum_fat = models.DecimalField(verbose_name='Сумма жиров', default=0, null=True, decimal_places=2, max_digits=20)
    sum_protein = models.DecimalField(verbose_name='Сумма белков', default=0, null=True, decimal_places=2, max_digits=20)
    sum_carbohydrate = models.DecimalField(verbose_name='Сумма углеводов', default=0, null=True, decimal_places=2, max_digits=20)

    def __str__(self):
        return f'Продукт: {self.product.name}'
    
    def save(self, *args, **kwargs):
        self.sum_calorie = self.quantity * self.product.calorie
        self.sum_fat = self.quantity * self.product.fat
        self.sum_protein = self.quantity * self.product.protein
        self.sum_carbohydrate = self.quantity * self.product.carbohydrate
        super(CartProduct, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Выбранный продукт'
        verbose_name_plural = 'Выбранные продукты'

    
class Cart(models.Model):
    owner = models.OneToOneField(Profile, verbose_name='Пользователь', on_delete=models.CASCADE)
    cart_products = models.ManyToManyField(
        CartProduct, blank=True, related_name='carts', verbose_name='Выбранные продукты'
    )
    total_calorie = models.DecimalField(verbose_name='Общее количество ккал', default=0, null=True, decimal_places=2, max_digits=20)
    total_fat = models.DecimalField(verbose_name='Общее количество жиров', default=0, null=True, decimal_places=2, max_digits=20)
    total_protein = models.DecimalField(verbose_name='Общее количество белков', default=0, null=True, decimal_places=2, max_digits=20)
    total_carbohydrate = models.DecimalField(verbose_name='Общее количество углеводов', default=0, null=True, decimal_places=2, max_digits=20)

    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        if self.id:
            self.total_calorie = sum([cproduct.sum_calorie for cproduct in self.cart_products.all()])
            self.total_fat = sum([cproduct.sum_fat for cproduct in self.cart_products.all()])
            self.total_protein = sum([cproduct.sum_protein for cproduct in self.cart_products.all()])
            self.total_carbohydrate = sum([cproduct.sum_carbohydrate for cproduct in self.cart_products.all()])
        super(Cart, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'