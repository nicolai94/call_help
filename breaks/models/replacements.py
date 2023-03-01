from django.contrib.auth import get_user_model
from django.db import models

from common.models.mixins import InfoMixin

User = get_user_model()


class GroupInfo(models.Model):
    group = models.OneToOneField(
        to='organisations.Group',
        on_delete=models.CASCADE,
        # related_name='break_info',
        verbose_name='Группа',
        primary_key=True  # ставлю в базе id именно группы
    )
    min_active = models.PositiveSmallIntegerField(
        verbose_name='Минимальное количество активных сотрудников',
        null=True,
        blank=True
    )
    break_start = models.TimeField(verbose_name='Начало обеда', null=True, blank=True)
    break_end = models.TimeField(verbose_name='Конец обеда', null=True, blank=True)
    break_max_duration = models.PositiveSmallIntegerField(
        verbose_name='Максимальная длительность обеда', null=True, blank=True
    )

    class Meta:
        verbose_name = 'Параметр обеденного перерыва'
        verbose_name_plural = 'Параметры обеденных перерывов'

    def __str__(self):
        return f'{self.group}'


class Replacement(InfoMixin):
    group = models.ForeignKey(
        to='breaks.GroupInfo',
        on_delete=models.CASCADE,
        related_name='replacements',
        verbose_name='Группа',
    )
    date = models.DateField(verbose_name='Дата смены')
    break_start = models.TimeField(verbose_name='Начало обеда')
    break_end = models.TimeField(verbose_name='Конец обеда')
    break_max_duration = models.PositiveSmallIntegerField(
        verbose_name='Макс. продолжительность обеда'
    )
    min_active = models.PositiveSmallIntegerField(
        verbose_name='Мин. число активных сотрудников', null=True, blank=True
    )
    members = models.ManyToManyField(
        'organisations.Member',
        related_name='replacements',
        through='ReplacementMember',
        verbose_name='Участник смены'
    )

    class Meta:
        verbose_name = 'Смена'
        verbose_name_plural = 'Смены'
        ordering = ('-date', )

    def __str__(self):
        return f' Смена № {self.pk} для ({self.group})'


class ReplacementMember(models.Model):
    member = models.ForeignKey(
        to='organisations.Member',
        on_delete=models.CASCADE,
        related_name='replacements_info',
        verbose_name='Сотрудник',
    )
    replacement = models.ForeignKey(
        to='breaks.Replacement',
        on_delete=models.CASCADE,
        related_name='members_info',
        verbose_name='Смена'
    )
    status = models.ForeignKey(
        to='breaks.ReplacementStatus',
        on_delete=models.RESTRICT,
        related_name='members',
        verbose_name='Статус'
    )

    class Meta:
        verbose_name = 'Смена - участник группы'
        verbose_name_plural = 'Смены - участники группы'

    def __str__(self):
        return f' Участник смены № {self.member.employee.user} ({self.pk})'


class ReplacementEmployee(models.Model):
    employee = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='replacements',
        verbose_name='Сотрудник',
    )
    replacement = models.ForeignKey(
        to='breaks.Replacement',
        on_delete=models.CASCADE,
        related_name='employees',
        verbose_name='Смена'
    )
    status = models.ForeignKey(
        to='breaks.ReplacementStatus',
        on_delete=models.RESTRICT,
        related_name='replacement_employees',
        verbose_name='Статус'
    )

    class Meta:
        verbose_name = 'Смена - Работник'
        verbose_name_plural = 'Смены - Работники'

    def __str__(self):
        return f' Смена № {self.replacement} для ({self.employee})'




