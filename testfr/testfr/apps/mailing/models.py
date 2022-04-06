from django.db import models
import pytz


class Property(models.Model):
    prop  = models.CharField('Property', max_length=25)
    def __str__(self):
        return self.prop

class Mailing(models.Model):
    start = models.DateTimeField('Start time')
    text = models.TextField('Text mailing')
    filter = models.ForeignKey(Property, on_delete=models.CASCADE)
    end = models.DateTimeField('End time')
    def __str__(self):
        return self.text

class Client(models.Model):
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    phone = models.IntegerField('Phone', blank=False)
    mnc = models.CharField('Mobile operator code', max_length=5)
    filter = models.ForeignKey(Property, on_delete=models.CASCADE, default=1)
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='Europe/Moscow')
    def __str__(self):
        return str(self.phone)

class Status(models.Model):
    status = models.CharField('Status', max_length=15)
    def __str__(self):
        return self.status

class Message(models.Model):
    time_send = models.DateTimeField("Sended time", auto_now_add=True)
    stat = models.ForeignKey(Status, on_delete=models.CASCADE)
    mailings = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    clients = models.ForeignKey(Client, on_delete=models.CASCADE)