from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь',
        primary_key=True # так как поле OTO то сделаем id будет юзер
    )
    telegram_id = models.CharField(max_length=20, verbose_name='Telegram ID', null=True, blank=True)

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профиль пользователей'

    def __str__(self):
        return f'{self.user} ({self.pk})'

