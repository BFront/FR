from django.db import models
import pytz

class Filters(models.Model):
    filter = models.CharField('Filter', max_length=15, default='')
    def __str__(self):
        return str(self.filter)

class Client(models.Model):
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    phone = models.CharField('Phone', max_length=12, unique=True)
    mnc = models.CharField('Mobile operator code', max_length=5)
    tag = models.ForeignKey(Filters, on_delete=models.CASCADE)
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='Europe/Moscow')
    def __str__(self):
        return str(self.phone)

class Mailing(models.Model):
    start = models.DateTimeField('Start time')
    text = models.TextField('Text mailing')
    filter = models.ForeignKey(Filters, on_delete=models.CASCADE)
    end = models.DateTimeField('End time')
    def __str__(self):
        return str(self.start)

class Status(models.Model):
    status = models.CharField('Status', max_length=15)
    def __str__(self):
        return self.status

class Message(models.Model):
    time_send = models.DateTimeField("Sended time", auto_now_add=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    mailings = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    clients = models.ForeignKey(Client, on_delete=models.CASCADE)