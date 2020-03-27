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
from school.views import index, AboutView, ComroomAdminView, make_room, reset_password, \
    send_password_mail
from timetable.views import assign_room

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('school/', include('school.urls')),
    # path('make_room/', make_room),
    # path('assign_room/', assign_room),
    path('send_password_mail/', send_password_mail, name='send_password_mail'),
    path('reset_password/<str:token>/', reset_password),
    path('comroom_admin/', ComroomAdminView.as_view()),
    path('ssam_ko/', AboutView.as_view(), name='about'),
    path('howto/', TemplateView.as_view(template_name="howto.html")),
    path('whatis/', TemplateView.as_view(template_name="whatis.html")),
    path('FAQ/', TemplateView.as_view(template_name="faq.html")),
    path('db_reset/', TemplateView.as_view(template_name="dbreset.html")),
    path('timetable/', include('timetable.urls', namespace='timetable')),

]
