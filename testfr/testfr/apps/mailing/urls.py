from django.urls import path
from . import views
urlpatterns =[
    path('api/clients/', views.client_list),
    path('api/clients/<int:pk>', views.client_detail),
]