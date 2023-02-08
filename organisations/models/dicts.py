from common.models.mixins import BaseDictModelMixin


class Position(BaseDictModelMixin):  # модель должности работника
    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'
