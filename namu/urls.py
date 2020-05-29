from django.urls import path

from .views import visitors, write, order, msg_test

app_name = 'namu'
urlpatterns = [
    path('visitors', visitors, name='visitors'),
    path('write', write, name='write_post'),
    path('order', order, name='order_page'),
    path('msg_test', msg_test, name='msg_test'),


]
