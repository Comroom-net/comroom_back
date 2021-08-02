from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    valid_scode_api,
    time_admin,
    FixCreateView,
    del_time,
    valid_scode,
    TimetableView,
    BookTime,
    del_fixed_time,
    TimetableViewSet,
    FixedTimetableViewSet,
)

router = DefaultRouter()
router.register(r"time", TimetableViewSet)
router.register(r"fixed", FixedTimetableViewSet)


app_name = "timetable"
urlpatterns = [
    path("api/", valid_scode_api),
    path("api/", include(router.urls)),
    path("time_admin/", time_admin),
    path("fix_time/", FixCreateView.as_view()),
    path("del_time/<int:i>", del_time),
    path("del_fixed_time/<int:i>", del_fixed_time),
    path("", valid_scode),
    path("<int:roomNo>/<date>/", TimetableView.as_view(), name="timetableView"),
    path("<int:pk>/<int:roomNo>/<date>/<int:time>/", BookTime.as_view()),
]
