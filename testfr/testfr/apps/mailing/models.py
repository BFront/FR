from django.db import models
import pytz

class Filters(models.Model):
    filter = models.CharField('Фильтр', max_length=15, default='')
    def __str__(self):
        return str(self.filter)
    class Meta:
        verbose_name = 'Фильтр'
        verbose_name_plural = 'Фильтры'

class Client(models.Model):
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    phone = models.CharField('Телефон', max_length=12, unique=True)
    mnc = models.CharField('Код мобильного оператора(непонятно зачем)', max_length=5)
    tag = models.ForeignKey(Filters, on_delete=models.CASCADE)
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='Europe/Moscow')
    def __str__(self):
        return str(self.phone)
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

class Mailing(models.Model):
    start = models.DateTimeField('Дата начала')
    text = models.TextField('Текст')
    filter = models.ForeignKey(Filters, on_delete=models.CASCADE)
    end = models.DateTimeField('Дата завершения')
    def __str__(self):
        return str(self.start)
    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

class Status(models.Model):
    status = models.CharField('Статус', max_length=15)
    def __str__(self):
        return self.status
    class Meta:
        verbose_name = 'Статус доставки'
        verbose_name_plural = 'Статусы доставки'

class Message(models.Model):
    time_send = models.DateTimeField("Время отправки", auto_now_add=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    mailings = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    clients = models.ForeignKey(Client, on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'