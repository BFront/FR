from rest_framework import serializers
from .models import *

class ClientsSerializer(serializers.ModelSerializer):
    # filter = serializers.ReadOnlyField(source='filter.prop')
    class Meta:
        model = Client
        fields = ('id',
                  'phone',
                  'mnc',
                  'filter',
                  'timezone')
