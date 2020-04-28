from django.urls import path

from .views import Nocookie, nocookie

app_name = 'etc'
urlpatterns = [
    path('nocookie', nocookie, name='nocookie'),
]
