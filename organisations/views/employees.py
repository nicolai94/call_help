from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.filters import SearchFilter, BaseFilterBackend

from common.views.mixins import LCRUDViewSet
from organisations.backends import OwnedByOrganisation
from organisations.filters import EmployeeFilter
from organisations.models.organisations import Employee
from organisations.permissions import IsColleagues
from organisations.serializers.api import employees as employees_s


@extend_schema_view(
    list=extend_schema(summary='Список сотрудников организации', tags=['Организации: Сотрудники']),
    retrieve=extend_schema(summary='Деталка сотрудника организации', tags=['Организации: Сотрудники']),
    create=extend_schema(summary='Создать сотрудника организации', tags=['Организации: Сотрудники']),
    update=extend_schema(summary='Изменить сотрудника организации', tags=['Организации: Сотрудники']),
    partial_update=extend_schema(summary='Изменить сотрудника организации частично', tags=['Организации: Сотрудники']),
    destroy=extend_schema(summary='Удалить сотрудника организации', tags=['Организации: Сотрудники']),
    search=extend_schema(filters=True, summary='Список сотружников органзации Search', tags=['Словари']),
)
class EmployeeView(LCRUDViewSet):
    queryset = Employee.objects.all()
    serializer_class = employees_s.EmployeeListSerializer
    permission_classes = [IsColleagues]
    multi_serializer_class = {
        'list': employees_s.EmployeeListSerializer,  # можно задать разное отображение для разных групп пользователей
        'retrieve': employees_s.EmployeeRetrieveSerializer,
        'create': employees_s.EmployeeCreateSerializer,
        'update': employees_s.EmployeeUpdateSerializer,
        'search': employees_s.EmployeeSearchSerializer,
        'partial_update': employees_s.EmployeeUpdateSerializer,
        'destroy': employees_s.EmployeeDeleteSerializer,
    }

    lookup_url_kwarg = 'employee_id'  # чтобы не было конфликта при вызове url адреса
    http_method_names = ('get', 'put', 'post', 'patch')

    filter_backends = (
        BaseFilterBackend,
        OrderingFilter,
        SearchFilter,
        OwnedByOrganisation,
    )
    filterset_class = EmployeeFilter
    ordering = ('position', 'date_joined', 'id')


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
        qs = Employee.objects.select_related(
            'user',
            'position',
        ).prefetch_related(
            'organisation',
        )
        return qs

    @action(methods=['GET'], detail=False, url_path='search')
    def search(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=dict())
        serializer.is_valid(raise_exception=True)
        return super().destroy(request, *args, **kwargs)
