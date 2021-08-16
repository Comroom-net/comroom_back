from django.urls import path

from .views import (
    msg_test_api,
    order_msg_api,
    visitors,
    write,
    order,
    msg_test,
    order_msg,
    order_success,
    room_auth,
    Namu_intro,
)

app_name = "namu"
urlpatterns = [
    path("api/msg-test/", msg_test_api),
    path("api/order/", order_msg_api),
    path("visitors", visitors, name="visitors"),
    path("write", write, name="write_post"),
    path("order", order, name="order_page"),
    path("msg_test", msg_test, name="msg_test"),
    path("order_msg", order_msg, name="order_msg"),
    path("order_success", order_success.as_view(), name="order_success"),
    path("room/<str:room>", room_auth, name="room_auth"),
    path("intro", Namu_intro.as_view(), name="introduction"),
]
