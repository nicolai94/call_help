

from django.contrib.auth.base_user import BaseUserManager
from rest_framework.exceptions import ParseError


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number=None, email=None, password=None, username=None, **extra_fields): # по умолчанию, чтобы ничего не сломалось
        if not (email or phone_number or username): # если нет ни email username phone_number тогда ошибка
            raise ParseError("Укажите email или телефон")
        if email: # если есть email то выдаем значение
            email = self.normalize_email(email)
        if not username:
            if email:
                username = email
            else:
                username = phone_number

        user = self.model(username=username, **extra_fields)
        if email: # присваеиваем значения
            user.email = email
        if phone_number:
            user.phone_number = phone_number
        user.set_password(password) # шифруем пароль в базе данных
        user.save(using=self._db) # сохраняем пароль для юзера в БД
        return user

    def create_user(self, phone_number=None,  email=None, password=None, username=None, **extra_fields): # по умолчанию, чтобы ничего не сломалось
        extra_fields.setdefault('is_superuser', False) # параметр админа
        extra_fields.setdefault('is_staff', False) # тоже для админа
        extra_fields.setdefault('is_active', True) # если вдруг неактивен

        return self._create_user(phone_number, email, password, username, **extra_fields)

    def create_superuser(self, phone_number=None, email=None, password=None, username=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True) # параметр админа
        extra_fields.setdefault('is_staff', True) # тоже для админа
        extra_fields.setdefault('is_active', True) # если вдруг неактивен

        return self._create_user(phone_number,email, password, username, **extra_fields)