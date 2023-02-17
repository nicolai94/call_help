import django_filters
from django.db.models import Q, F

from organisations.constants import DIRECTOR_POSITION, MANAGER_POSITION
from organisations.models.groups import Group
from organisations.models.offers import Offer
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
    can_be_group_manager = django_filters.BooleanFilter(
        method='can_be_group_manager_filter', label='Can be group manager'
    )

    class Meta:
        model = Employee
        fields = ('only_corporate',)

    def can_be_group_manager_filter(self, queryset, name, value):
        return queryset.filter(position_id__in=[DIRECTOR_POSITION, MANAGER_POSITION])


class GroupFilter(django_filters.FilterSet):  # фильтр по группам
    is_member = django_filters.BooleanFilter(
        field_name='is_member',
    )

    class Meta:
        model = Group
        fields = ('organisation', 'manager', 'is_member')


class OfferOrgFilter(django_filters.FilterSet):
    TYPE_CHOICES = (
        ('sent', 'Отправленные'),
        ('received', 'Полученные')
    )
    DECISION_CHOICES = (
        ('accept', 'Принятые'),
        ('reject', 'Отклоненные'),
        ('unknown', 'Не рассмотрении'),
    )

    can_accept = django_filters.BooleanFilter('can_accept', )
    can_reject = django_filters.BooleanFilter('can_reject', )

    type = django_filters.ChoiceFilter(
        method='type_filter',
        choices=TYPE_CHOICES,
        label='type',
    )
    decision = django_filters.ChoiceFilter(
        method='decision_filter',
        choices=DECISION_CHOICES,
        label='decision',
    )

    class Meta:
        model = Offer
        fields = ('user_accept', )

    def type_filter(self, queryset, name, value):
        if value == 'sent':
            return queryset.filter(~Q(created_by=F('user'))) # те поля поля в которых created_by != юзеру
        elif value == 'received':
            return queryset.filter(created_by=F(''))  # только те которы были созданы юзером
        return queryset

    def decision_filter(self, queryset, name, value):
        offer_type = self.data.get('type')  # узнаю значение из другого фильтра
        if offer_type not in ['sent', 'received']:
            return queryset
        if value not in ['accept', 'reject', 'unknown']:
            return queryset

        sent_type = bool(offer_type == 'sent')
        decision_filter = {
            # в зависимости от принятого типа засылаю улсовие для фильтрации
            'accept': Q(user_accept=True) if sent_type else Q(org_accept=True),
            'reject': Q(user_accept=False) if sent_type else Q(org_accept=False),
            'unknown': Q(user_accept=None) if sent_type else Q(org_accept=None),
        }
        return queryset.filter(decision_filter[value])


class OfferUserFilter(django_filters.FilterSet):
    TYPE_CHOICES = (
        ('sent', 'Отправленные'),
        ('received', 'Полученные'),
    )
    DECISION_CHOICES = (
        ('accept', 'Принятые'),
        ('reject', 'Отклоненные'),
        ('unknown', 'На рассмотрении'),
    )

    can_accept = django_filters.BooleanFilter('can_accept',)
    can_reject = django_filters.BooleanFilter('can_reject',)

    type = django_filters.ChoiceFilter(
        method='type_filter',
        choices=TYPE_CHOICES,
        label='type',
    )

    decision = django_filters.ChoiceFilter(
        method='decision_filter',
        choices=DECISION_CHOICES,
        label='decision',
    )

    class Meta:
        model = Offer
        fields = ('user_accept',)

    def type_filter(self, queryset, name, value):
        if value == 'sent':
            return queryset.filter(created_by=F('user'))
        elif value == 'received':
            return queryset.filter(~Q(created_by=F('user')))
        return queryset

    def decision_filter(self, queryset, name, value):
        offer_type = self.data.get('type')
        if offer_type not in ['sent', 'received']:
            return queryset
        if value not in ['accept', 'reject', 'unknown']:
            return queryset

        sent_type = bool(offer_type == 'sent')
        decision_filter = {
            'accept': Q(user_accept=True) if sent_type else Q(org_accept=True),
            'reject': Q(user_accept=False) if sent_type else Q(org_accept=False),
            'unknown': Q(user_accept=None) if sent_type else Q(org_accept=None),
        }
        return queryset.filter(decision_filter[value])