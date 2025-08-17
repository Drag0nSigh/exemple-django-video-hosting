import logging

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from core.constants import MAX_LENGTH_EMAIL, MAX_LENGTH_USERS_CHAR


logger = logging.getLogger('models')


class User(AbstractUser):
    username = models.CharField(
        verbose_name='Никнейм',
        max_length=MAX_LENGTH_USERS_CHAR,
        unique=True,
        help_text=f'Обязательное поле. Никнейм. Максимальная длина {MAX_LENGTH_USERS_CHAR} символов.',
        blank=False,
        null=False,
        validators=[UnicodeUsernameValidator()],
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=MAX_LENGTH_EMAIL,
        unique=True,
        help_text='Обязательное поле. Введите корректный адрес электронной почты.',
        blank=False,
        null=False,
    )
    first_name = models.CharField(
        verbose_name='Имя пользователя',
        max_length=MAX_LENGTH_USERS_CHAR,
        help_text='Обязательное поле. Имя пользователя.',
        blank=False,
        null=False,
    )
    last_name = models.CharField(
        verbose_name='Фамилия пользователя',
        max_length=MAX_LENGTH_USERS_CHAR,
        help_text='Обязательное поле. Фамилия пользователя.',
        blank=False,
        null=False,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
