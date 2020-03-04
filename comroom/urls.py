"""comroom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from school.views import RegisterView
from timetable.views import TimetableView, valid_scode, BookingView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RegisterView.as_view()),
    path('comroom/', valid_scode),
    path('comroom/<int:pk>/<int:roomNo>/',
         TimetableView.as_view(), name='timetable'),
    path('comroom/<int:pk>/<int:roomNo>/<int:year>/<int:month>/<int:day>/<int:time>/',
         BookingView.as_view())
]
