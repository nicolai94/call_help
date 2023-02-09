import django_filters

from organisations.models.groups import Group
from organisations.models.organisations import Organisation, Employee


class OrganisationFilter(django_filters.FilterSet):  # собственный фильтр для поля can_manage
    can_manage = django_filters.BooleanFilter(field_name='can_manage', label='Can manage')  # поле для создания фильтра

    class Meta:
        model = Organisation
        fields = ('can_manage', 'id')


class EmployeeFilter(django_filters.FilterSet):  # фильтр по корпоративным сотрудникам по парам is_corporate_account
    only_corporate = django_filters.BooleanFilter(
        field_name='user__is_corporate_account', label='Is corporate account'
    )

    class Meta:
        model = Employee
        fields = ('only_corporate',)


class GroupFilter(django_filters.FilterSet):  # фильтр по группам
    is_member = django_filters.BooleanFilter(
        field_name='is_member',
    )

    class Meta:
        model = Group
        fields = ('organisation', 'manager', 'is_member')
