import os
import requests
import time

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from bs4 import BeautifulSoup
from pytils.translit import slugify

from calorie.models import Category, Product


class Command(BaseCommand):
    help = 'Parsing data from the site'

    def handle(self, *args, **options):
        url = settings.URL
        soup = self.__get_page(url)

        all_categories = soup.find_all('div', class_='main_block') + soup.find_all('divi', class_='main_block')

        categories_name = {}
        categories_image = {}
        categories_url = {}

        for category in all_categories:
            cat_url = category.find('a').get('href')
            num = int(cat_url.split("=")[-1])

            cat_url = url + cat_url
            categories_url[num] = cat_url
            
            cat_name = category.find('div', class_='menu_name')
            categories_name[num] = cat_name.text

            cat_image = category.find('img')
            cat_image_url = url + cat_image.attrs.get('src')
            categories_image[num] = cat_image_url

        path_to_files = os.path.join(settings.BASE_DIR, 'media/category')

        for key, value in categories_image.items():
            name_image = slugify(categories_name[key])
            img_link = value

            if not os.path.exists(path_to_files):
                os.makedirs(path_to_files)
            with open(os.path.join(path_to_files, f'{name_image}.png'), "wb") as f:
                    f.write(requests.get(img_link).content)

        for key, value in categories_name.items():
            cat_name = value
            cat_img_name = slugify(cat_name)
            cat_img ='category/' + f'{cat_img_name}.png'
            try:
                new_category = Category(name=cat_name, photo=cat_img)
                new_category.save()
            except IntegrityError:
                print('This object is already exists')

        products_name = {}
        path_to_files = os.path.join(settings.BASE_DIR, 'media/product')
        for key, value in categories_url.items():
            soup = self.__get_page(value)
            all_products = soup.find_all('div', class_='product')
            all_bgu = soup.find_all('table', class_='info_table')
            category = categories_name[key]
            count = 0

            for product in all_products:
                data_product = {}
                product_name = product.find('div', class_='product_name').text
                try:
                    kkal_product = float(all_bgu[count].find('span', class_='kkal_visible').text)
                    protein_product = float(all_bgu[count].find('span', class_='bel_visible').text)
                    fat_product = float(all_bgu[count].find('span', class_='fat_visible').text)
                    carbohydrate_product = float(all_bgu[count].find('span', class_='ug_visible').text)
                except ValueError:
                    continue

                count += 1

                product_img = product.find('img')
                product_img_url = url + product_img.attrs.get('src')

                img_name = slugify(product_name)
                slug_category = slugify(category)
                path_to_product_img = path_to_files + '/' + slug_category

                if not os.path.exists(path_to_product_img):
                    os.makedirs(path_to_product_img )
                with open(os.path.join(path_to_product_img,  f'{img_name}.png'), "wb") as f:
                    f.write(requests.get(product_img_url).content)

                product_img_path = f'product/{slug_category}/{img_name}.png'

                data_product['kkal'] = kkal_product
                data_product['protein'] = protein_product
                data_product['fat'] = fat_product
                data_product['carbohydrate'] = carbohydrate_product
                data_product['photo'] = product_img_path
                data_product['category'] = category

                products_name[product_name] = data_product

        for product, data in products_name.items():
            product_img = data['photo']
            kkal = data['kkal']
            protein = data['protein']
            fat = data['fat']
            carbohydrate = data['carbohydrate']
            name = product

            category = Category.objects.get(name=data['category'])

            try:
                new_product = Product(
                    name=name, 
                    photo=product_img,
                    calorie=kkal,
                    fat=fat,
                    protein=protein,
                    carbohydrate=carbohydrate,
                    category=category
                )
                new_product.save()
            except IntegrityError:
                print('This object is already exists')
        
        print('Parsing finished')

    def __get_page(self, url):
        page = requests.get(url)
        if page.status_code != 200:
            time.sleep(5)
            self.__get_page(url)

        soup = BeautifulSoup(page.text, 'html.parser')
        if soup.text == 'Не удалось соединится с базой данных':
            time.sleep(5)
            self.__get_page(url)
        
        return soup