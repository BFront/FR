from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *

# https://webdevblog.ru/sozdanie-django-api-ispolzuya-django-rest-framework-apiview/
class ClientView(APIView):
    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response({"clients": serializer.data})
    def post(self, request):
        client = request.data.get('clients')
        serializer = ClientSerializer(data=client)
        if serializer.is_valid(raise_exception=True):
            client_saved = serializer.save()
        return Response({"success": "Client '{}' created successfully".format(client_saved.title)})

# @api_view(['GET', 'POST', 'DELETE'])
# def client_list(request):
#     if request.method == 'GET':
#         clients = Client.objects.all()
#         clients_serializer = ClientsSerializer(clients, many=True)
#         return JsonResponse(clients_serializer.data, safe=False)
#     elif request.method == 'POST':
#         client_data = JSONParser().parse(request)
#         client_serializer = ClientsSerializer(data=client_data)
#         if client_serializer.is_valid():
#             client_serializer.save()
#             return JsonResponse(client_serializer.data, status=status.HTTP_201_CREATED)
#         return JsonResponse(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         count = Client.objects.all().delete()
#         return JsonResponse({'message': '{} Client delete.'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def client_detail(request, pk):
#     try:
#         client = Client.objects.get(pk=pk)
#     except Client.DoesNotExist:
#         return JsonResponse({'message': 'The client does not exist'}, status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         client_serializer = ClientsSerializer(client)
#         return JsonResponse(client_serializer.data)
#     elif request.method == 'PUT':
#         client_data = JSONParser().parse(request)
#         client_serializer = ClientsSerializer(client, data=client_data)
#         if client_serializer.is_valid():
#             client_serializer.save()
#             return JsonResponse(client_serializer.data)
#         return JsonResponse(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         client.delete()
#         return JsonResponse({'message': 'Client was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

