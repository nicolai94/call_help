from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from common.models.mixins import InfoMixin

User = get_user_model()


class Group(InfoMixin):
    organisation = models.ForeignKey(
        to='Organisation',
        on_delete=models.RESTRICT,
        related_name='groups',
        verbose_name='Организация'
    )
    name = models.CharField('Название', max_length=255) # db_column='name'
    manager = models.ForeignKey(
        to=User,
        on_delete=models.RESTRICT,
        related_name='groups_managers',
        verbose_name='Менеджер',
    )
    employees = models.ManyToManyField(
        to=User,
        related_name='groups_employees',
        verbose_name='Сотрудники',
        blank=True
    )
    members = models.ManyToManyField(
        to=User,
        related_name='groups_members',
        verbose_name='Участники группы',
        blank=True,
        through='Member',
    )
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('name', )

    def __str__(self):
        return f'{self.name} ({self.pk})'


class Member(models.Model):  # участник
    group = models.ForeignKey(
        to='Group',
        on_delete=models.CASCADE,
        related_name='members_info',
        verbose_name='Участник'
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='groups_info',
        verbose_name='Пользователь',
    )
    date_joined = models.DateField('Date joined', default=timezone.now)

    class Meta:
        verbose_name = 'Участник группы'
        verbose_name_plural = 'Участники групп'
        ordering = ('-date_joined', )
        unique_together = (('group', 'user'), )
        # указываем какие поля должны быть уникальны совместно, чтобы нельзя было создать несколько раз одно и то же

    def __str__(self):
        return f'Member {self.user}'
