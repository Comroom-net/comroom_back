from django.urls import path

from .views import (
    send_telegram
)

app_name = "common"

urlpatterns = [
    path("send-msg/", send_telegram),
]
