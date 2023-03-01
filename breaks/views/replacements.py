from django.db.models import Count, Case, When, Q
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.filters import SearchFilter, BaseFilterBackend

from breaks.factory.replacements import ReplacementFactory
from breaks.models.replacements import Replacement
from common.views.mixins import CRUDViewSet
from breaks.serializers.api import replacements as replacements_s


@extend_schema_view(
    list=extend_schema(summary='Список смен', tags=['Обеды: Смены']),
    retrieve=extend_schema(summary='Деталка смены', tags=['Обеды: Смены']),
    create=extend_schema(summary='Создать смену', tags=['Обеды: Смены']),
    partial_update=extend_schema(summary='Изменить группу частично', tags=['Обеды: Смены']),

)
class ReplacementView(CRUDViewSet):
    queryset = Replacement.objects.all()
    serializer_class = replacements_s.ReplacementListSerializer
    # permission_classes = [IsMyReplacement]
    multi_serializer_class = {
        'list': replacements_s.ReplacementListSerializer,
        'retrieve': replacements_s.ReplacementRetrieveSerializer,
        'create': replacements_s.ReplacementCreateSerializer,
        'partial_update': replacements_s.ReplacementUpdateSerializer,
    }

    http_method_names = ('get', 'post', 'patch')

    filter_backends = (
        OrderingFilter,
        DjangoFilterBackend,
        # MyReplacement
    )
    # filterset_class = ReplacementFilter

    def get_queryset(self):
        return ReplacementFactory().list()


