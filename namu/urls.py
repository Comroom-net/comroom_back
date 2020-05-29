from django.urls import path

from .views import visitors, write, order

app_name = 'namu'
urlpatterns = [
    path('visitors', visitors, name='visitors'),
    path('write', write, name='write_post'),
    path('order', order, name='order_page')

]
