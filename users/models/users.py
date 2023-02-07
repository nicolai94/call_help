from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

from users.managers import CustomUserManager
from users.models.profile import Profile


class User(AbstractUser): # наследуемся от базового класса
    username = models.CharField(null=True, blank=True, verbose_name='Никнейм', unique=True, max_length=255)
    email = models.EmailField(max_length=255, verbose_name='Почта', unique=True, null=True)
    phone_number = PhoneNumberField(verbose_name='Телефон', unique=True, null=True)  # библиотека phonenumberfields

    USERNAME_FIELD = 'username' # поле для выбора авторизации
    REQUIRED_FIELDS = ['email'] # указание какие поля должны быть обязательными

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.full_name} ({self.pk})'


@receiver(post_save, sender=User)  # использование сигналов
def post_save_user(sender, instance, created, **kwargs):
    if not hasattr(instance, 'profile'):  # проверяем есть ли у юзера созданный профиль через related_name
        Profile.objects.create(user=instance)  # если нет, то создаем новый

