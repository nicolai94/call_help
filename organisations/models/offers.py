from django.contrib.auth import get_user_model
from django.db import models

from common.models.mixins import InfoMixin

User = get_user_model()


class Offer(InfoMixin):  # модель оффера
    organisation = models.ForeignKey(
        to='Organisation',
        on_delete=models.RESTRICT,
        related_name='offers',
        verbose_name='Организация'
    )
    org_accept = models.BooleanField(
        null=True, blank=True, verbose_name='Согласие организации'
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.RESTRICT,
        related_name='offers',
        verbose_name='Пользователь'
    )
    user_accept = models.BooleanField(
        null=True, blank=True, verbose_name='Согласие пользователя'
    )

    class Meta:
        verbose_name = 'Оффер'
        verbose_name_plural = 'Офферы'
        ordering = ('-created_at', )
        unique_together = (('organisation', 'user'), )

    def __str__(self):
        return f'Оффер №{self.pk}'

    @property
    def is_from_org(self):  # возвращает тру или фолс при проверке эта заявка от организации пользователя
        return bool(self.user != self.created_by) # ЕСЛИ ТРУ то организация отправляла

    @property
    def is_from_user(self):
        return bool(self.user == self.created_by) # ЕСЛИ ТРУ то юзер отправляла
