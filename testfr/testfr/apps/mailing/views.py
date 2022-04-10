import time
from datetime import datetime
import requests
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import *

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        r.headers["accept"] = "application/json"
        r.headers["Content-Type"] = "application/json"
        return r

def cron(request):
    mails = Mailing.objects.filter(start__lte = datetime.now(), end__gte = datetime.now())
    for q in range(0, mails.count()):
        otvet = startMessages(request, mails[q].id, mails[q].filter_id)
    return otvet

def startMessages(request, pk, filter):
    clients = Client.objects.filter(tag=filter)
    mailing = Mailing.objects.get(pk=pk)
    msgid = 1
    for q in clients:
        check = Message.objects.filter(clients_id=q.id, mailings_id=pk, status_id=1).count()
        print(check)
        if check == 0:
            # timing = round(time.time()-1649570000)
            data = {"id": int(msgid), "phone": int(q.phone), "text": str(mailing.text)}
            response = requests.post("https://probe.fbrq.cloud/v1/send/"+str(msgid), json=data, auth=BearerAuth(
                'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODA3NzIxODksImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6IkBqdWRtZW50X3RnIn0.7-omHSNXaIuP9RT1-HzMhoO9Vd9qQAY-_ftrSVreYxM'))

            if response.status_code == 200:
                status = 1 #STATUS OK
                msgid += 1
            else:
                status = 4 #STATUS ERROR
            print(f'{msgid} - {response.status_code} - {response.request} - {data}')
            check_err = Message.objects.filter(clients_id=q.id, mailings_id=pk, status_id=status).count()
            if check_err == 0:
                Message.objects.create(clients_id=q.id, mailings_id=pk, status_id=status)
    return HttpResponse(status=200)

@api_view(['GET',])
def statistic_full(request, type):
    statistic = {}
    if request.method == 'GET':
        if type == 'mailings':
            mailings = Mailing.objects.all()
            messages_ok = Message.objects.filter(status=1).count()
            messages_error = Message.objects.filter(status=4).count()
            statistic['mailings_all'] = mailings.count()
            statistic['messages_all'] = messages_ok+messages_error
            statistic['messages_ok'] = messages_ok
            statistic['messages_error'] = messages_error
        elif type == 'messages':
            s = Message.objects.all().count()
            statistic['messages'] = s
        elif type == 'clients':
            s = Client.objects.all().count()
            statistic['clients'] = s
        else:
            statistic['err'] = 'Unknow TYPE'
    return JsonResponse(statistic)
@api_view(['GET',])
def statistic_detail(request, type, pk):
    try:
        messages = Message.objects.filter(mailings_id=pk)
        messages_out = Message.objects.filter(mailings_id=pk, status=1).count()
        messages_error = Message.objects.filter(mailings_id=pk, status=4).count()
        mailing = Mailing.objects.get(pk=pk)
    except Message.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    statistic = {}
    if request.method == 'GET':
        if type == 'mailing':
            statistic['mailing_start'] = str(mailing.start)
            statistic['mailing_end'] = str(mailing.end)
            statistic['mailing_filter'] = str(mailing.filter)
            statistic['mailing_text'] = mailing.text
            statistic['messages_all'] = messages_out+messages_error
            statistic['messages_ok'] = messages_out
            statistic['messages_error'] = messages_error
        else:
            statistic['err'] = 'Unknow TYPE'
    return JsonResponse(statistic)

@api_view(['GET', 'POST'])
def clients_list(request):
    if request.method == 'GET':
        snippets = Client.objects.all()
        serializer = ClientSerializer(snippets, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET', 'POST'])
def mailings_list(request):
    if request.method == 'GET':
        snippets = Mailing.objects.all()
        serializer = MailingSerializer(snippets, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MailingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET', 'POST'])
def messages_list(request):
    if request.method == 'GET':
        snippets = Message.objects.all()
        serializer = MessageSerializer(snippets, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def client_detail(request, pk):
    try:
        snippet = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ClientSerializer(snippet)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ClientSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
@api_view(['GET', 'PUT', 'DELETE'])
def mailing_detail(request, pk):
    try:
        snippet = Mailing.objects.get(pk=pk)
    except Mailing.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = MailingSerializer(snippet)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = MailingSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
@api_view(['GET', 'PUT', 'DELETE'])
def message_detail(request, pk):
    try:
        snippet = Message.objects.get(pk=pk)
    except Message.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = MessageSerializer(snippet)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = MessageSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)