from django.db import models
from django.urls import reverse
from pytils.translit import slugify



def product_directory_path(instance, filename):
    return f'product/{instance.category.name}/{filename}'


class Category(models.Model):
    name = models.CharField(verbose_name='Название категории', max_length=255)
    photo = models.ImageField(verbose_name='Изображение категории', upload_to='category/')
    slug = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(verbose_name='Название продукта', max_length=255)
    photo = models.ImageField(verbose_name='Изображение продукта', upload_to=product_directory_path) 
    calorie = models.FloatField(verbose_name='Ккал')
    fat = models.FloatField(verbose_name='Жиры')
    protein = models.FloatField(verbose_name='Белки')
    carbohydrate = models.FloatField(verbose_name='Углеводы')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return f'{self.name} - {self.category.name}'
    
    def get_absolute_url(self):
        return reverse('product', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'