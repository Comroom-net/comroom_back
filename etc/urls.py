from django.urls import path

from .views import nocookie, GsuiteConvertor, load_html, load_last_html

app_name = 'etc'
urlpatterns = [
    path('nocookie', nocookie, name='nocookie'),
    path('g-suite', GsuiteConvertor, name='GsuiteConvertor'),
    path('page', load_last_html, name='page'),
    path('page/<int:pk>', load_html, name='page'),

]
