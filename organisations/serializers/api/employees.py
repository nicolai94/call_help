import pdb

from crum import get_current_user
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.transaction import atomic
from rest_framework import serializers

from rest_framework.exceptions import ParseError

from common.serializers.mixins import ExtendedModelSerializer
from organisations.models.organisations import Organisation, Employee

User = get_user_model()


class EmployeeListSerializer(ExtendedModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeRetrieveSerializer(ExtendedModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeCreateSerializer(ExtendedModelSerializer):
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Employee
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
            'position',
        )

        # передается словарь со значениями а мы преобразуем в нужные, чтобы не отсылать все PUT
    def validate(self, attrs):
        current_user = get_current_user()  # получаю текущего юзера из зарпоса
        organisation_id = self.context['view'].kwargs.get('pk')  # получаю id  со страницы
        organisation = Organisation.objects.filter(
            id=organisation_id, director=current_user).first()  # проверяю на наличие в бд
        #  проверка что пользователь - владелец организации
        if not organisation:
            raise ParseError(
                'Такой организации не найдено'
            )
        attrs['organisation'] = organisation
        return attrs

    def create(self, validated_data):
        # создаю данные из validated data
        user_data = {
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
            'email': validated_data.pop('email'),
            'password': validated_data.pop('password'),
            'is_corporate_account': True,
        }
        with transaction.atomic():
            # создаю нового юзера
            user = User.objects.create_user(**user_data)
            # передаю в data
            validated_data['user'] = user
            # сохраняю instance
            instance = super().create(validated_data)
        return instance


class EmployeeUpdateSerializer(ExtendedModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'




