from django.urls import path
from .views import ClientView
app_name = "mailing"
urlpatterns = [
    path('client/', ClientView.as_view()),
    path('client/<int:pk>', ClientView.as_view())
]