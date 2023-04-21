FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /caloriemanagement

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY requirements.txt /caloriemanagement/
RUN pip install -r requirements.txt

COPY . /caloriemanagement/
EXPOSE 6000