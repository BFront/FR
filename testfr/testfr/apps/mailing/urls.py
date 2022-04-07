from django.urls import path
from . import views
urlpatterns =[
    path('api/clients/', views.snippet_list),
    path('api/client/<int:pk>', views.snippet_detail),
]