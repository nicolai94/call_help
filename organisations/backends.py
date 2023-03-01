from django.db.models import Q
from rest_framework.filters import BaseFilterBackend


class OwnedByOrganisation(BaseFilterBackend):  # чтобы могли увидеть только сотрудников нужной организации
    def filter_queryset(self, request, queryset, view):
        org_id = request.parser_context['kwargs'].get('pk')
        return queryset.filter(organisation_id=org_id)


class OwnedByGroup(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        group_id = request.parser_context['kwargs'].get('pk')
        return queryset.filter(organisation_id=group_id)

class MyOrganisation(BaseFilterBackend):  # кастомный бэкенд для фильтра чтобы оставить среди всех организаций, где текущий пользователь директор либо сотрудник
    def filter_queryset(self, request, queryset, view):
        user = request.user
        return queryset.filter(
            Q(director=user) | Q(employees=user)
        )  # можно и в view, но лучше перенес


class MyGroup(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        return queryset.filter(
            Q(organisation__director=user) | Q(organisation__employees=user))
