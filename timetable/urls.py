from django.urls import path

from .views import time_admin, FixCreateView, del_time, valid_scode, TimetableView, BookTime

app_name = 'timetable'
urlpatterns = [
    path('time_admin/', time_admin),
    path('fix_time/', FixCreateView.as_view()),
    path('del_time/<int:i>', del_time),
    path('', valid_scode),
    path('<int:roomNo>/<date>/',
         TimetableView.as_view(), name='timetableView'),
    path('<int:pk>/<int:roomNo>/<date>/<int:time>/',
         BookTime.as_view())
]
