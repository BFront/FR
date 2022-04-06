from django.contrib import admin
from .models import *

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'prop')

class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'start', 'text', 'filter', 'end')
    list_filter = ('filter',)

class ClientAdmin(admin.ModelAdmin):
    list_display = ('phone', 'mnc', 'filter', 'timezone')

class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'status')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('time_send', 'mailings', 'clients', 'stat')
    list_filter = ('stat',)


admin.site.register(Property, PropertyAdmin)
admin.site.register(Mailing, MailingAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Message, MessageAdmin)

