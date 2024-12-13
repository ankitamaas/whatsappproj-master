from django.urls import path
from . import views

urlpatterns = [
    path("", views.send_whatsapp_messages, name="send_whatsapp_messages"),
]
