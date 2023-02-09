from django.db.models import Count, Case, When, Q
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.filters import SearchFilter, BaseFilterBackend
from common.views.mixins import CRUDViewSet
from organisations.backends import OwnedByOrganisation, MyGroup
from organisations.filters import EmployeeFilter, GroupFilter
from organisations.models.groups import Group
from organisations.models.organisations import Employee
from organisations.permissions import IsColleagues, IsMyGroup
from organisations.serializers.api import groups as group_s


@extend_schema_view(
    list=extend_schema(summary='Список групп', tags=['Организации: Группы']),
    retrieve=extend_schema(summary='Деталка группы', tags=['Организации: Группы']),
    create=extend_schema(summary='Создать группу', tags=['Организации: Группы']),
    update=extend_schema(summary='Изменить группу', tags=['Организации: Группы']),
    partial_update=extend_schema(summary='Изменить группу частично', tags=['Организации: Группы']),
)
class GroupView(CRUDViewSet):
    queryset = Group.objects.all()
    serializer_class = group_s.GroupListSerializer
    permission_classes = [IsMyGroup]
    multi_serializer_class = {
        'list': group_s.GroupListSerializer,  # можно задать разное отображение для разных групп пользователей
        'retrieve': group_s.GroupRetrieveSerializer,
        'create': group_s.GroupCreateSerializer,
        'update': group_s.GroupUpdateSerializer,
        'partial_update': group_s.GroupUpdateSerializer
    }

    http_method_names = ('get', 'post', 'patch')

    filter_backends = (
        OrderingFilter,
        SearchFilter,
        DjangoFilterBackend,
        MyGroup
    )
    search_fields = ('name',)
    filterset_class = GroupFilter
    ordering = ('name', 'id')

    # def get_serializer_class(self):  # переопределить метод сериализаторов
    #     if self.action == 'retrieve':  # method GET
    #         return employees_s.EmployeeRetrieveSerializer
    #     elif self.action == 'create':  # method POST
    #         return employees_s.EmployeeCreateSerializer
    #     elif self.action == 'update':  # method PUT
    #         return employees_s.EmployeeUpdateSerializer
    #     elif self.action == 'partial_update':  # method PATCH
    #         return employees_s.EmployeeUpdateSerializer
    #     return self.serializer_class

    def get_queryset(self):  # фильтрую всех сотрудников и отбираю тех кто по id совпадает с текущим, кто меняет из URL
        queryset = Group.objects.select_related(
            'manager',
        ).prefetch_related(
            'organisation',
            'organisation__director',
            'members'
        ).annotate(  # на уровне бд добавил данные
            pax=Count('members', distinct=True),  # distinct уникальное
            can_manage=Case(  # определяю условие по кейсам
                When(
                    Q(manager__user=self.request.user) |
                    Q(organisation__director=self.request.user),
                    then=True,
                ),
                default=False,
            ),
            is_member=Case(
                When(Q(members_info__employee__user=self.request.user), then=True),
                # захожу в список всех member_info по related_name
                default=False,
            ),
        )
        return queryset
