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
from django.urls import path, include
from django.views.generic import TemplateView
from school.views import index, AboutView, ComroomAdminView, make_room, time_admin, del_time
from timetable.views import TimetableView, valid_scode, assign_room, BookTime, FixCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('school/', include('school.urls')),
    path('make_room/', make_room),
    path('assign_room/', assign_room),
    path('comroom_admin/', ComroomAdminView.as_view()),
    path('time_admin/', time_admin),
    path('fix_time/', FixCreateView.as_view()),
    path('del_time/<int:i>', del_time),
    path('ssam_ko/', AboutView.as_view(), name='about'),
    path('howto/', TemplateView.as_view(template_name="howto.html")),
    path('whatis/', TemplateView.as_view(template_name="whatis.html")),
    path('FAQ/', TemplateView.as_view(template_name="faq.html")),
    path('db_reset/', TemplateView.as_view(template_name="dbreset.html")),
    path('comroom/', valid_scode),
    path('comroom/<int:roomNo>/<date>/',
         TimetableView.as_view(), name='timetable'),
    path('comroom/<int:pk>/<int:roomNo>/<date>/<int:time>/',
         BookTime.as_view())
]
