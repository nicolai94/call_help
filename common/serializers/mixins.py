from rest_framework import serializers

from users.serializers.nested.users import UserShortSerializer


class ExtendedModelSerializer(serializers.ModelSerializer):  # миксин сериализатора
    class Meta:
        abstract = True


class DictMixinSerializer(serializers.Serializer):  # миксин для статусов
    code = serializers.CharField()
    name = serializers.CharField()


class InfoModelSerializer(ExtendedModelSerializer):
    created_by = UserShortSerializer()
    updated_by = UserShortSerializer()

    class Meta:
        abstract = True