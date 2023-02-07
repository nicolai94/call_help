from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ParseError

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)  # параметр не отображает запись при возврате  # allow blank, allow true, required параметры пропустить, null и обязательность, writeOnly только для записи

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


class ChangePasswordSerializer(serializers.Serializer):
    pass
