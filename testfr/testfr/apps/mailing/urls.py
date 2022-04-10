from django.urls import path
from . import views


urlpatterns = [
    path('statistic/<str:type>', views.statistic_full),
    path('statistic/<str:type>/<int:pk>', views.statistic_detail),
    path('clients/', views.clients_list),
    path('client/<int:pk>', views.client_detail),
    path('mailings/', views.mailings_list),
    path('mailing/<int:pk>', views.mailing_detail),
    path('messages/', views.messages_list),
    path('message/<int:pk>', views.message_detail),
    path('cron/', views.cron)
]