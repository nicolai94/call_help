from django.db import models
from django.utils import timezone

from config import settings


class BaseDictModelMixin(models.Model):
    code = models.CharField(verbose_name='Код', max_length=16, primary_key=True)
    name = models.CharField(verbose_name='Название', max_length=32)
    sort = models.PositiveSmallIntegerField(verbose_name='Сортировка', null=True, blank=True)
    is_active = models.BooleanField(verbose_name='Активность', default=True)

    class Meta:
        ordering = ('sort', )
        abstract = True  # don't create migration, because we take for this model abstract class

    def __str__(self):
        return f'{self.code} ({self.name})'


class DateMixin(models.Model): # миксин для времени создания и обновления
    created_at = models.DateTimeField(verbose_name='Created at', null=True, blank=False)
    updated_at = models.DateTimeField(verbose_name='Updated at', null=True, blank=False)

    class Meta:
        abstract = True  # класс является абстрактным и не создает обьект, только для наследования

    def save(self, *args, **kwargs):  # логика сохранения и проверка при сохранении
        if not self.id and not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(DateMixin, self).save(*args, **kwargs)


class InfoMixin(DateMixin): # миксин для отображения создания и обновления чего-либо
    created_by = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='created_%(app_label)s_%(class)s',  # чтобы related name был уникален при любом классе
        verbose_name='Created by',
        null=True
    )
    updated_by = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='updated_%(app_label)s_%(class)s',
        verbose_name='Updated by',
        null=True
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        from crum import get_current_user  # пакет чтобы получить текущего юзера в миксине
        user = get_current_user()
        if user and not user.pk: # если что то есть в юзере но нет id, то ничего не записываю
            user = None
        if not self.pk:
            self.created_by = user
        self.updated_by = user
        super().save(*args, **kwargs)
