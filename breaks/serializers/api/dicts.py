from django.contrib.auth import get_user_model

from breaks.models.dicts import ReplacementStatus, BreakStatus
from common.serializers.mixins import ExtendedModelSerializer, DictMixinSerializer

User = get_user_model()

# Заменил на миксин

# class ReplacementStatusListSerializer(DictMixinSerializer):  # сериализатор смен
#     pass
#
#
# class BreakStatusListSerializer(DictMixinSerializer):  # сериализатор перерыва
#     pass


