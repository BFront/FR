import datetime

from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import *

def cron(request):

    mails = Mailing.objects.filter(start__lte = datetime.datetime.now(), end__gte = datetime.datetime.now())
    s = {}
    for q in range(0, mails.count()):
        print(mails[q].start)
        s['start'] = str(mails[q].start)
        s['stop'] = str(mails[q].end)
    return JsonResponse(s)
    # return HttpResponse(status=200)

def startMailing(request, pk):
    try:
        mailing = Mailing.objects.get(pk=pk)
    except Mailing.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    s = {}
    filter = mailing.filter
    date_end = mailing.end
    date_now = datetime.datetime.now()

    print(date_end.strftime("%d.%m.%y %I:%M"))
    print(date_now.strftime("%d.%m.%y %I:%M"))
    if date_end > date_now:
        print("+")
    #check date


    clients = Client.objects.filter(tag=filter)
    # for q in clients:
        # Message.objects.create(clients_id=q.id, mailings_id=pk, status_id=1)

    return JsonResponse(s)
@api_view(['GET',])
def statistic_full(request, type):
    statistic = {}
    if request.method == 'GET':
        if type == 'mailings':
            mailings = Mailing.objects.all()
            messages= Message.objects.all()
            messages_out = Message.objects.filter(status=1)
            messages_sended = Message.objects.filter(status=2)
            messages_read = Message.objects.filter(status=3)
            messages_error = Message.objects.filter(status=4)
            statistic['mailings_all'] = mailings.count()
            statistic['messages_all'] = messages.count()
            statistic['messages_out'] = messages_out.count()
            statistic['messages_sended'] = messages_sended.count()
            statistic['messages_read'] = messages_read.count()
            statistic['messages_error'] = messages_error.count()
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
        messages_sended = Message.objects.filter(mailings_id=pk, status=2).count()
        messages_read = Message.objects.filter(mailings_id=pk, status=3).count()
        messages_error = Message.objects.filter(mailings_id=pk, status=4).count()
        mailing = Mailing.objects.get(pk=pk)
    except Message.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    statistic = {}
    if request.method == 'GET':
        if type == 'mailings':
            statistic['mailing_start'] = str(mailing.start)
            statistic['mailing_end'] = str(mailing.end)
            statistic['mailing_filter'] = str(mailing.filter)
            statistic['mailing_text'] = mailing.text
            statistic['messages_out'] = messages_out
            statistic['messages_sended'] = messages_sended
            statistic['messages_read'] = messages_read
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