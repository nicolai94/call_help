from rest_framework import serializers


class ReplacementStatsSerializer(serializers.Serializer):
    created_pax = serializers.IntegerField()
    confirmed_pax = serializers.IntegerField()
    on_break_pax = serializers.IntegerField()
    finished_pax = serializers.IntegerField()
    canceled_pax = serializers.IntegerField()