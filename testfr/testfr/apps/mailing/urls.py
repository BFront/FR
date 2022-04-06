from django.urls import path
from . import views
urlpatterns =[
    path('api/clients/', views.GetClients.as_view()),
    path('api/client/<int:id>', views.GetClient.as_view()),
]