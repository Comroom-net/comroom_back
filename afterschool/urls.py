from django.urls import path

from .views import apply_page

app_name = 'afterschool'
urlpatterns = [
    path('apply', apply_page, name='apply'),


]
