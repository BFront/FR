from rest_framework import serializers

class ClientSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=12)
    mnc = serializers.CharField(max_length=5)
    filter = serializers.CharField(source='filter.prop', max_length=32)
    timezone = serializers.CharField(max_length=32)