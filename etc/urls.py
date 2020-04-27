from django.urls import path

from .views import Nocookie

app_name = 'etc'
urlpatterns = [
    path('nocookie', Nocookie.as_view(), name='nocookie'),
]
