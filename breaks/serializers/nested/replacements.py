from crum import get_current_user
from django.utils import timezone
from rest_framework import serializers

from breaks.models.replacements import GroupInfo, Replacement, ReplacementMember
from breaks.serializers.internal.breaks import BreakForReplacementSerializer
from common.serializers.mixins import ExtendedModelSerializer, InfoModelSerializer, DictMixinSerializer


class BreakSettingsSerializer(ExtendedModelSerializer):
    class Meta:
        model = GroupInfo
        exclude = ('group', )


class ReplacementShortSerializer(InfoModelSerializer):

    class Meta:
        model = Replacement
        exclude = (
            'id',
            'date',
            'break_start',
            'break_end',
            'break_max_duration',
            'min_active',
        )


class ReplacementMemberShortSerializer(ExtendedModelSerializer):
    id = serializers.CharField(source='member.employee.user.pk')
    full_name = serializers.CharField(source='member.employee.user.full_name')
    username = serializers.CharField(source='member.employee.user.username')
    email = serializers.CharField(source='member.employee.user.email')
    status = DictMixinSerializer()

    class Meta:
        model = ReplacementMember
        fields = (
            'id',
            'full_name',
            'username',
            'email',
            'status',
        )

class ReplacementBreakSerializer(serializers.Serializer):
    info = serializers.SerializerMethodField()
    button = serializers.SerializerMethodField()

    def get_info(self, instance):
        user = get_current_user()
        break_obj = instance.get_break_for_user(user)
        return BreakForReplacementSerializer(break_obj, allow_null=True).data

    def get_button(self, instance):
        user = get_current_user()
        return instance.get_break_status_for_user(user)


class ReplacementActionSerializer(serializers.Serializer):
    replacement_button = serializers.SerializerMethodField()
    break_button = serializers.SerializerMethodField()

    def get_replacement_button(self, instance):
        now = timezone.now().astimezone()
        if instance.date != now.date():
            return None
        user = get_current_user()
        member = instance.get_member_by_user(user)
        if not member:
            return None

    def get_button(self, instance):
        user = get_current_user()
        return instance.get_break_status_for_user(user)