from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model



User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='Пользователь', on_delete=models.CASCADE)
