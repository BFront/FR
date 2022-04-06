from rest_framework import serializers

class ClientSerializer(serializers.Serializer):
    phone = serializers.IntegerField()
    mnc = serializers.CharField(max_length=5)
    filter = serializers.ReadOnlyField(source='filter.prop')
    timezone = serializers.CharField(max_length=32)