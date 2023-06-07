import os
import requests

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from bs4 import BeautifulSoup
from pytils.translit import slugify

from calorie.models import Category


class Command(BaseCommand):
    help = 'Parsing data from the site'

    def handle(self, *args, **options):
        url = settings.URL
        main_page = requests.get(url)
        soup = BeautifulSoup(main_page.text, 'html.parser')

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
