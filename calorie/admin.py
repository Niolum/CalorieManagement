from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Product, Category



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.photo.url} width="100" height="100"')
    
    get_image.short_descripton = 'Изображение'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'calorie', 'fat', 'protein', 'carbohydrate', 'slug', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.photo.url} width="100" height="100"')

    get_image.short_description = 'Изображение'