from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *

class GetClients(APIView):
    def get(self, request):
        queryset = Client.objects.all()
        serializer_for_queryset = ClientSerializer(
            instance=queryset,
            many=True
        )
        return Response(serializer_for_queryset.data)

class GetClient(APIView):
    def get(self, request, id):
        queryset = Client.objects.get(id=id)
        serializer_for_queryset = ClientSerializer(
            instance=queryset,
            many=False
        )
        return Response(serializer_for_queryset.data)
