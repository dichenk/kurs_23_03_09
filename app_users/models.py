from django.contrib.auth.models import AbstractUser
from django.db import models
from config import settings


class Users(AbstractUser):
    username = models.CharField(max_length=50, verbose_name='имя пользователя', unique=True)
    email = models.EmailField(verbose_name='почта', unique=True)
    
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username}\n'

