from drf_spectacular.utils import extend_schema_view, extend_schema

from common.views.mixins import CRUDViewSet
from organisations.models.organisations import Employee
from organisations.serializers.api import employees as employees_s


@extend_schema_view(
    list=extend_schema(summary='Список сотрудников организации', tags=['Организации: Сотрудники']),
    retrieve=extend_schema(summary='Деталка сотрудника организации', tags=['Организации: Сотрудники']),
    create=extend_schema(summary='Создать сотрудника организации', tags=['Организации: Сотрудники']),
    update=extend_schema(summary='Изменить сотрудника организации', tags=['Организации: Сотрудники']),
    partial_update=extend_schema(summary='Изменить сотрудника организации частично', tags=['Организации: Сотрудники']),
    destroy=extend_schema(summary='Удалить сотрудника организации', tags=['Организации: Сотрудники']),
)
class EmployeeView(CRUDViewSet):
    queryset = Employee.objects.all()
    serializer_class = employees_s.EmployeeListSerializer

    lookup_url_kwarg = 'employee_id'  # чтобы не было конфликта при вызове url адреса

    def get_serializer_class(self):  # переопределить метод сериализаторов
        if self.action == 'retrieve':  # method GET
            return employees_s.EmployeeRetrieveSerializer
        elif self.action == 'create':  # method POST
            return employees_s.EmployeeCreateSerializer
        elif self.action == 'update':  # method PUT
            return employees_s.EmployeeUpdateSerializer
        elif self.action == 'partial_update':  # method PATCH
            return employees_s.EmployeeUpdateSerializer
        return self.serializer_class

    def get_queryset(self):  # фильтрую всех сотрудников и отбираю тех кто по id совпадает с текущим, кто меняет из URL
        organisation_id = self.request.parser_context['kwargs'].get('pk')  # получить id из URL
        queryset = Employee.objects.filter(
            organisation_id=organisation_id
        )
        return queryset
