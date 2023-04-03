from re import M

from breaks.models.breaks import Break
from common.serializers.mixins import ExtendedModelSerializer


class BreakForReplacementSerializer(ExtendedModelSerializer):
    class Meta:
        model = Break
        fields = (
            'id',
            'break_start',
            'break_end',
        )
        #   меняю формат времени
        extra_kwargs = {
            'break_start': {'format': '%H:%M'},
            'break_end': {'format': '%H:%M'},
        }