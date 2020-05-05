from django.urls import path

from .views import visitors, write

app_name = 'namu'
urlpatterns = [
    path('visitors', visitors, name='visitors'),
    path('write', write, name='write_post')

]
