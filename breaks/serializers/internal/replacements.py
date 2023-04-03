import datetime

from crum import get_current_user
from rest_framework import serializers
from breaks.models.replacements import ReplacementMember, Replacement
from breaks.serializers.api.groups import GroupShortSerializer
from breaks.serializers.internal.breaks import BreakForReplacementSerializer
from common.serializers.mixins import ExtendedModelSerializer


# здесь кастомные сериализаторы

class ReplacementStatsSerializer(serializers.Serializer):
    all_pax = serializers.IntegerField()
    break_pax = serializers.IntegerField()
    confirmed_pax = serializers.IntegerField()
    on_break_pax = serializers.IntegerField()
    finished_pax = serializers.IntegerField()
    canceled_pax = serializers.IntegerField()


class ReplacementGeneralSerializer(ExtendedModelSerializer):
    group = GroupShortSerializer(source='group.group')
    break_start = serializers.TimeField(format='%H:%M')
    break_end = serializers.TimeField(format='%H:%M')
    date = serializers.DateField(format='%d.%m.%Y')

    class Meta:
        model = Replacement
        fields = (
            'id',
            'group',
            'date',
            'break_start',
            'break_end',
            'break_max_duration',
            'min_active',
        )


class ReplacementPersonalStatsSerializer(serializers.Serializer):
    time_online = serializers.DateTimeField(format='%H:%M')
    time_break_start = serializers.DateTimeField(format='%H:%M')
    time_break_end = serializers.DateTimeField(format='%H:%M')
    time_offline = serializers.DateTimeField(format='%H:%M')
    time_until_break = serializers.SerializerMethodField()

    class Meta:
        model = ReplacementMember
        fields = (
            'time_online',
            'time_break_start',
            'time_break_end',
            'time_offline',
            'time_until_break',
        )

    def get_time_until_break(self, instance):   # выбираем для определеннгого участника и смены время до обеденноого перерыва
        now = datetime.datetime.now().time()
        break_obj = instance.breaks.filter(replacement=instance.replacement).first()
        if not break_obj:
            return None

        now = datetime.datetime.now().time()
        now_minutes = now.hour * 60 + now.minute
        break_minutes = break_obj.break_start.hour * 60 + break_obj.break_start.minute

        delta = break_minutes - now_minutes
        if delta < 0:
            return None

        delta_hour = delta // 60
        delta_minute = delta % 60
        result = f'{delta_hour // 10} {delta_hour % 10}:{delta_minute // 10}{delta_minute % 10}'
        return result


class ReplacementBreaksSerializer(serializers.Serializer):
    info = serializers.SerializerMethodField()
    button = serializers.SerializerMethodField()

    def get_info(self, instance):
        user = get_current_user()
        break_obj = instance.get_break_for_user(user)
        return BreakForReplacementSerializer(break_obj, allow_null=True).data

    def get_button(self, instance):
        user = get_current_user()
        return instance.get_break_for_user(user)