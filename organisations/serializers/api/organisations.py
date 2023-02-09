import pdb

from crum import get_current_user
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.exceptions import ParseError

from common.serializers.mixins import ExtendedModelSerializer
from organisations.constants import DIRECTOR_POSITION
from organisations.models.organisations import Organisation
from users.serializers.nested.users import UserShortSerializer

User = get_user_model()


class OrganisationSearchListSerializer(ExtendedModelSerializer):
    director = UserShortSerializer()

    class Meta:
        model = Organisation
        fields = (
            'id',
            'name',
            'director',
        )


class OrganisationListSerializer(ExtendedModelSerializer):  # просмотр только своих организаций
    director = UserShortSerializer()

    class Meta:
        model = Organisation
        fields = '__all__'


class OrganisationRetrieveSerializer(ExtendedModelSerializer):  #
    director = UserShortSerializer()

    class Meta:
        model = Organisation
        fields = '__all__'


class OrganisationCreateSerializer(ExtendedModelSerializer):

    class Meta:
        model = Organisation
        fields = ('id', 'name')

    def validate_name(self, value): # проверка на имя организации
        if self.Meta.model.objects.filter(name=value):
            raise ParseError(
                'Организация с таким названием уже существует'
            )
        return value

    def validate(self, attrs): # при создании организации, создающий автоматически ее директор
        user = get_current_user()
        attrs['director'] = user
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            instance = super().create(validated_data)
            instance.employees.add(  # когда создаю организацию то автоматически добавляю сотрудника в должность директора
                validated_data['director'],
                through_defaults={'position_id': DIRECTOR_POSITION}
            )
        return instance


class OrganisationUpdateSerializer(ExtendedModelSerializer):

    class Meta:
        model = Organisation
        fields = ('id', 'name')







