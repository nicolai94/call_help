from django.db.models import Count, Case, When
from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

from common.views.mixins import ListViewSet, CRUDViewSet, CRUViewSet
from organisations.backends import MyOrganisation
from organisations.filters import OrganisationFilter
from organisations.models.organisations import Organisation
from organisations.permissions import IsMyOrganisation
from organisations.serializers.api import organisations


@extend_schema_view(  # автодокументация для spectacular
    list=extend_schema(summary='Список организаций Search', tags=['Словари']),)
class OrganisationSearchView(ListViewSet):
    queryset = Organisation.objects.all()
    serializer_class = organisations.OrganisationSearchListSerializer


@extend_schema_view(
    list=extend_schema(summary='Список организаций', tags=['Организации']),
    retrieve=extend_schema(summary='Деталка организаций', tags=['Организации']),
    create=extend_schema(summary='Создать организацию', tags=['Организации']),
    update=extend_schema(summary='Изменить организацию', tags=['Организации']),
    partial_update=extend_schema(summary='Изменить организацию частично', tags=['Организации']),

)
class OrganisationView(CRUViewSet):  # сделали свой сет
    permission_classes = [IsMyOrganisation]
    multi_permissions_classes = {  # возможность для каждого метода задать permission
        'list': [IsMyOrganisation | IsAuthenticated]
    }
    queryset = Organisation.objects.all()
    serializer_class = organisations.OrganisationListSerializer
    multi_serializer_class = {
        'admin__list': organisations.OrganisationListSerializer,  # можно задать разное отображение для разных групп пользователей
        'operator__list': organisations.OrganisationListSerializer,
        'retrieve': organisations.OrganisationRetrieveSerializer,
        'create': organisations.OrganisationCreateSerializer,
        'update': organisations.OrganisationUpdateSerializer,
        'partial_update': organisations.OrganisationUpdateSerializer
    }
    http_method_names = ('get', 'post', 'patch')
    filter_backends = (
        OrderingFilter,
        SearchFilter,
        DjangoFilterBackend,  # появляется возможность определить filterset_fields(class)
        MyOrganisation,
    )
    search_fields = ('name', )
    filterset_class = OrganisationFilter
    ordering = ('name', 'id')

    def get_queryset(self):
        queryset = Organisation.objects.select_related(
            'director',  # все элементы по пути director
        ).prefetch_related(
            'employees',
            'groups',
        ).annotate(  # на уровне бд добавил данные
            pax=Count('employees', distinct=True),  # distinct уникальное
            groups_count=Count('groups', distinct=True),
            can_manage=Case(  # определяю условие по кейсам
                When(director=self.request.user, then=True),
                default=False,
            )
        )
        return queryset

    # def get_serializer_class(self):  # переопределить метод сериализаторов
    #     if self.action == 'retrieve':  # method GET
    #         return organisations.OrganisationRetrieveSerializer
    #     elif self.action == 'create':  # method POST
    #         return organisations.OrganisationCreateSerializer
    #     elif self.action == 'update':  # method PUT
    #         return organisations.OrganisationUpdateSerializer
    #     elif self.action == 'partial_update':  # method PATCH
    #         return organisations.OrganisationUpdateSerializer
    #     return self.serializer_class


