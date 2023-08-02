# CalorieManagement

![Static Badge](https://img.shields.io/badge/python-3.11-blue?logo=python&link=https%3A%2F%2Fwww.python.org%2F)
![Static Badge](https://img.shields.io/badge/django-4%2C2-%23092E20?logo=django&link=https%3A%2F%2Fwww.djangoproject.com%2F)
![Static Badge](https://img.shields.io/badge/DRF-3%2C14-%23ED1C24?link=https%3A%2F%2Fwww.django-rest-framework.org%2F)
![Coverage Status](https://img.shields.io/badge/coverage-97%25-%23f5d442)



## About Project

CalorieManagement is an API for counting calories. It implements site parsing (https://supercalorizator.ru/). Categories, products and their calories, proteins, fats and carbohydrates, as well as pictures of categories and products are parsed from this site. Implemented the ability to register a user, create a cart for the user (in which products are added to count calories), as well as receive products and categories.


## Features
- **[Python](https://www.python.org/)** (version 3.11)
- **[Django](https://www.djangoproject.com/)**
- **[DRF](https://www.django-rest-framework.org/)**
- **[PostgreSQL](https://www.postgresql.org/)**
- **[Docker Compose](https://docs.docker.com/compose/)**

## Quickstart

First, clone project

``` 
git clone https://github.com/Niolum/CalorieManagement.git
```

Further, set up the virtual environment and the main dependencies from the ``requirements.txt``

```
python -m venv venv
source venv/bin/activate 
pip install -r requirements.txt
```

Then, create .env file. set environment variables and create database.

Example ``.env``:

```
DBUSER=username
DBPASS=password
DBNAME=db_name
DBHOST=localhost
DBPORT=5432

DEBUG=0
SECRET_KEY='some_secret_key'
DJANGO_ALLOWED_HOSTS="*"

URL='https://supercalorizator.ru/'
```

Before starting, you need to execute several commands:

```
python manage.py migrate
python manage.py scrapy
```

Run application:

```
python manage.py runserver
```

For start in docker-compose change .env:

```
POSTGRES_USER=username
POSTGRES_PASSWORD=password
POSTGRES_DB=db_name

DBUSER=username
DBPASS=password
DBNAME=db_name
DBHOST=postgres
DBPORT=5432

DEBUG=0
SECRET_KEY='some_secret_key'
DJANGO_ALLOWED_HOSTS="*"

URL='https://supercalorizator.ru/'
```

Before running docker-compose:

```
docker volume create caloriedb
docker volume create calorie_media
```

To start the project, use the following command:

```
docker-compose up -d
```

## Run test


To run all the tests of a project, simply run the pytest command:

```
pytest
```