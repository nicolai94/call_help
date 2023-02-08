from rest_framework import serializers


class ExtendedModelSerializer(serializers.ModelSerializer):  # миксин сериализатора
    class Meta:
        abstract = True


class DictMixinSerializer(serializers.Serializer):  # миксин для статусов
    code = serializers.CharField()
    name = serializers.CharField()
