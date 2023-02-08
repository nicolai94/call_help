from drf_spectacular.utils import extend_schema_view, extend_schema

from common.serializers.mixins import DictMixinSerializer
from common.views.mixins import ListViewSet, DictListMixin
from breaks.models.dicts import ReplacementStatus, BreakStatus
from breaks.serializers.api import dicts as dicts_s


@extend_schema_view(
    list=extend_schema(summary='Список статусов смен', tags=['Словари']),)
class ReplacementStatusView(DictListMixin):  # миксином задали сериализатор
    queryset = ReplacementStatus.objects.filter(is_active=True)


@extend_schema_view(
    list=extend_schema(summary='Список статусов обеденных перерывов', tags=['Словари']),)
class BreakStatusView(DictListMixin):
    queryset = BreakStatus.objects.filter(is_active=True)