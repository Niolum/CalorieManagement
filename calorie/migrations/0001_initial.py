# Generated by Django 4.2 on 2023-06-12 12:35

import calorie.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название категории')),
                ('photo', models.ImageField(upload_to='category/', verbose_name='Изображение категории')),
                ('slug', models.SlugField(max_length=160, unique=True)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название продукта')),
                ('photo', models.ImageField(max_length=255, upload_to=calorie.models.product_directory_path, verbose_name='Изображение продукта')),
                ('calorie', models.FloatField(verbose_name='Ккал')),
                ('fat', models.FloatField(verbose_name='Жиры')),
                ('protein', models.FloatField(verbose_name='Белки')),
                ('carbohydrate', models.FloatField(verbose_name='Углеводы')),
                ('slug', models.SlugField(max_length=160, unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calorie.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
    ]
