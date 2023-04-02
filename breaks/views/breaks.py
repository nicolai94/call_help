from django.db.models import Q
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.generics import RetrieveUpdateAPIView, get_object_or_404
from rest_framework.response import Response

from breaks.models.breaks import Break
from breaks.models.replacements import Replacement
from breaks.services import get_schedule_time_title
from common.views.mixins import ExtendedCRUAPIView, ListViewSet
from breaks.serializers.api import breaks as breaks_s
from users.permissions import IsNotCorporate


@extend_schema_view(  # автодокументация для spectacular
    get=extend_schema(summary='Деталка обеда', tags=['Обеды: обеды пользователя']),
    post=extend_schema(summary='Резерв обеда', tags=['Обеды: обеды пользователя']),
    patch=extend_schema(summary='Изменение резерва обеда', tags=['Обеды: обеды пользователя'])
)
class BreakMeView(ExtendedCRUAPIView):  # показ и изменение профиля пользователя
    queryset = Break.objects.all()
    http_method_names = ('get', 'post', 'patch')  # для того чтобы убрать метод put и работать только patch
    serializer_class = breaks_s.BreakMeRetrieveSerializer
    multi_serializer_class = {
        'GET': breaks_s.BreakMeRetrieveSerializer,
        'POST': breaks_s.BreakMeCreateSerializer,
        'PATCH': breaks_s.BreakMeUpdateSerializer
    }

    # permission_classes = [IsNotCorporate]  # только для зарегистрированный

    def get_object(self):  # выбираем только те перерывы которые нам доступны
        user = self.request.user
        replacement_id = self.request.parser_contex['kwargs'].get('pk')
        # qs = Break.objects.filter(replacement_id=replacement_id, member__employee__user=user).first()
        return get_object_or_404(
            Break, Q(replacement_id=replacement_id, member__member__employee__user=user)
        )


@extend_schema_view(
    list=extend_schema(summary='Расписание обедов', tags=['Обеды: Обеды'])
)
class BreakScheduleView(ListViewSet):   # вью для расписания перерывов и преобразования для фронта
    # permission_classes = [IsNotCorporate]
    queryset = Break.objects.all()
    serializer_class = breaks_s.BreakScheduleSerializer
    pagination_class = None

    def list(self, request, *args, **kwargs):
        replacement_id = self.request.parser_contex['kwargs'].get('pk')
        replacement = get_object_or_404(Replacement, id=replacement_id)
        title = get_schedule_time_title(
            replacement.break_start, replacement.break_end, 'Сотрудник'
        )
        qs = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(qs, many=True).data
        serializer.insert(0, title)
        return Response(serializer)

    def get_queryset(self):
        replacement_id = self.request.parser_contex['kwargs'].get('pk')
        return Break.objects.prefetch_related(
            'member',
            'member__member',
            'member__member__employee',
            'member__member__employee__user',
        ).filter(replacement_id=replacement_id)


