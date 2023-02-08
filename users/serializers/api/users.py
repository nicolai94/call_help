from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from users.serializers.nested.profile import ProfileShortSerializer, ProfileUpdateSerializer

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):  # Регистрация
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True)  # параметр не отображает запись при возврате  # allow blank, allow true, required параметры пропустить, null и обязательность, writeOnly только для записи

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
        )

    # вся логика в сериализаторе
    # валидация email
    def validate_email(self, value):
        email = value.lower()  # приводим к нижнему регистру email
        if User.objects.filter(email=email).exists():  # проверяем в базе
            raise ParseError(  # вызываем ошибку
                'Пользователь с такой почтой уже зарегистрирован.'
            )
        return email  # возвращаем данные

    # валидация пароля
    def validate_password(self, value):
        validate_password(value)  # используем метод встроенной валидации
        return value

    def create(self, validated_data):  # создание нового пароля при изменении и ШИФРУЕМ его
        user = User.objects.create_user(**validated_data)
        return user


class ChangePasswordSerializer(serializers.ModelSerializer):  # Смена пароля ( в профиле должны нажать кнопку и ввести пароль, а потом только сменить его)
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password')

    def validate(self, attrs):
        user = self.instance  # принимаемые данные
        old_password = attrs.pop('old_password')  # достаю из словаря old_password
        if not user.check_password(old_password):  # автоматически проверят пароль
            raise ParseError(
                'Проверьте правильность текущего пароля'
            )
        return attrs

    def validate_new_password(self, value):  # валидация нового пароля
        validate_password(value)
        return value

    # обновление модели паролей
    def update(self, instance, validated_data):
        password = validated_data.pop('new_password')  # значение validateddata приходит из attrs
        instance.set_password(password)  # шифровка пароля в бд
        instance.save()
        return instance


class MeSerializer(serializers.ModelSerializer): # для GET запросов
    profile = ProfileShortSerializer()  # nested сериалайзер для внутренних данных

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'username',
            'profile',
            'date_joined',
        )


class MeUpdateSerializer(serializers.ModelSerializer):  # для PUT PATCH запросов
    profile = ProfileUpdateSerializer()

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'username',
            'profile',
            'date_joined',
        )

    def update(self, instance, validated_data): # переопределяю update чтобы записывать данные внутри
        # Проверка наличия профиля
        profile_data = validated_data.pop('profile') if 'profile' in validated_data else None  # проверка на ошибки если нет данных

        with transaction.atomic():  # создание транзакции для обновления значений
            instance = super().update(instance, validated_data) # дальше по умолчанию сделать update
            # Update профиля
            if profile_data:
                self._update_profile(profile=instance.profile, data=profile_data)
        return instance

    def _update_profile(self, profile, data): # сделал внутреннюю функцию и вызвал сверху
        # Update профиля
        # то же что и             for key, value in profile_data.items():
        #                 if hasattr(profile, key):  # есть ли в profile значения key
        #                     setattr(profile, key, value)  # меняем в profile значения на key и value
        #             profile.save()
        profile_serializer = ProfileUpdateSerializer(instance=profile, data=data,
                                                     partial=True)  # partial частичное изменение
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()


class UserSearchListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'full_name',
        )
