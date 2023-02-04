import uuid

from django.contrib.auth import get_user_model
from django.db import models

from breaks.constants import BREAK_CREATED_STATUS, BREAK_CREATED_DEFAULT
from breaks.models.dicts import BreakStatus

User = get_user_model()


class Break(models.Model):
    replacement = models.ForeignKey(
        to='breaks.Replacement',
        on_delete=models.CASCADE,
        related_name='breaks',
        verbose_name='Смена'
    )
    employee = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='breaks',
        verbose_name='Сотрудник',
    )
    break_start = models.TimeField(verbose_name='Начало обеда', null=True, blank=True)
    break_end = models.TimeField(verbose_name='Конец обеда', null=True, blank=True)
    status = models.ForeignKey(
        to='breaks.BreakStatus',
        on_delete=models.RESTRICT,
        related_name='breaks',
        verbose_name='Статус',
        blank=True
    )

    class Meta:
        verbose_name = 'Обеденный перерыв'
        verbose_name_plural = 'Обеденные перерывы'
        ordering = ('-replacement__date', 'break_start')

    def __str__(self):
        return f'Обед пользователя {self.employee} ({self.pk})'

    def save(self, *args, **kwargs):
        if not self.pk: # проверка на создание 1 раз, есть ли id
            status, created = BreakStatus.objects.get_or_create( # в случае если обьекта нет то создаем обьект, иаче просто еберем его
                code=BREAK_CREATED_STATUS,
                defaults=BREAK_CREATED_DEFAULT
            )
            self.status = status
            # self.status = BreakStatus.objects.filter(code=BREAK_CREATED_STATUS).first() # сразу задаем статус из константы
        return super().save(*args, **kwargs)





