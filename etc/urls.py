from django.urls import path

from .views import nocookie, GsuiteConvertor

app_name = 'etc'
urlpatterns = [
    path('nocookie', nocookie, name='nocookie'),
    path('g-suite', GsuiteConvertor, name='GsuiteConvertor'),
]
