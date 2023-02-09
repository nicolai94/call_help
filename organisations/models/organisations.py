import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from common.models.mixins import InfoMixin
from organisations.constants import DIRECTOR_POSITION

User = get_user_model()


class Organisation(InfoMixin):
    name = models.CharField('Название', max_length=255)
    director = models.ForeignKey(
        to=User,
        on_delete=models.RESTRICT,
        related_name='organisations_directors',  # при переносе модели нужно заменить related_name
        verbose_name='Директор',
    )
    employees = models.ManyToManyField(
        to=User,
        related_name='organisations_employees',  # при переносе модели нужно заменить related_name
        verbose_name='Сотрудники',
        blank=True,
        through='Employee',  # когда обращаемся к этому поле, то можем работать как с M2M
    )

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
        ordering = ('name', )

    def __str__(self):
        return f'{self.name} ({self.pk})'

    @property
    def director_employee(self):  # проверка в организации того, что
        obj, create = self.employees_info.get_or_create(
            position_id=DIRECTOR_POSITION, defaults={'user': self.director,}
        )
        return obj


class Employee(models.Model):  # должность
    organisation = models.ForeignKey(
        to='Organisation',
        on_delete=models.CASCADE,
        related_name='employees_info',
        verbose_name='Сотрудник'
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='organisations_info',
        verbose_name='Пользователь',
    )
    position = models.ForeignKey(
        to='Position',
        on_delete=models.RESTRICT,
        related_name='employees',
        verbose_name='Должность',
    )
    date_joined = models.DateField('Date joined', default=timezone.now)

    class Meta:
        verbose_name = 'Сотрудник организации'
        verbose_name_plural = 'Сотрудники организации'
        ordering = ('-date_joined', )
        unique_together = (('organisation', 'user'), )
        # указываем какие поля должны быть уникальны совместно, чтобы нельзя было создать несколько раз одно и то же

    def __str__(self):
        return f'Employee {self.user}'

