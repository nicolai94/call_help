import pdb

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView

from users.serializers.api import users as user_s

User = get_user_model()


@extend_schema_view(  # автодокументация для spectacular
    post=extend_schema(summary='Регистрация пользователя', tags=['Аутентификация & Авторизация']),
)
class RegistrationView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]  # разрешает всем
    serializer_class = user_s.RegistrationSerializer


@extend_schema_view(
    post=extend_schema(request=user_s.ChangePasswordSerializer,  # показывает какие поля отправляются
        summary='Смена пароля', tags=['Аутентификация & Авторизация']),
)
class ChangePasswordView(APIView):

    def post(self, request):
        user = request.user # получаем юзера из присланных данных
        serializer = user_s.ChangePasswordSerializer(  # записываем данные в сериализатор
            instance=user, data=request.data  # обновляем обьект юзера
        )
        # pdb.set_trace()  # использую для дебаггинга
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_204_NO_CONTENT)


@extend_schema_view(  # автодокументация для spectacular
    get=extend_schema(summary='Профиль пользователя', tags=['Пользователи']),
    put=extend_schema(summary='Изменить профиль пользователя', tags=['Пользователи']),
    patch=extend_schema(summary='Изменить частично профиль пользователя', tags=['Пользователи'])
)
class MeView(RetrieveUpdateAPIView):  # показ и изменение профиля пользователя
    queryset = User.objects.all()
    serializer_class = user_s.MeSerializer
    http_method_names = ('get', 'patch')  # для того чтобы убрать метод put и работать только patch

    def get_serializer_class(self):  # переопределить метод сериализаторов
        if self.request.method in ['PUT', 'PATCH']: # условие для изменения
            return user_s.MeUpdateSerializer
        return user_s.MeSerializer

    def get_object(self):
        return self.request.user


