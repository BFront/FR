from django.contrib import admin
from .models import *

class FilterAdmin(admin.ModelAdmin):
    list_display = ('id', 'filter')


class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'start', 'text', 'filter', 'end')
    list_filter = ('filter',)

class ClientAdmin(admin.ModelAdmin):
    list_display = ('phone', 'mnc', 'tag', 'timezone')

class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'status')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('time_send', 'mailings', 'clients', 'status')
    list_filter = ('status',)


admin.site.register(Filters, FilterAdmin)
admin.site.register(Mailing, MailingAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Message, MessageAdmin)

