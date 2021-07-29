from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    SchoolView,
    ex_login_api,
    user_active_api,
    login,
    logout,
    forgot_password,
    privacy_agree,
    agree_pirv,
    RegisterView,
    user_active,
    ex_login,
    MultipleFormsLoginView,
    SchoolViewSet,
    ComroomViewSet,
    AdminUserViewSet,
    NoticeViewSet,
)

app_name = "school"

router = DefaultRouter()
router.register(r"comroom", ComroomViewSet)
router.register(r"admin-user", AdminUserViewSet)
router.register(r"notice", NoticeViewSet)
router.register(r"", SchoolViewSet)

urlpatterns = [
    path("api/login/", login),
    path("api/forgot-password/", forgot_password),
    path("api/ex_login/", ex_login_api),
    path("api/register/", SchoolView.as_view()),
    path("api/active/<token>", user_active_api),
    path("login/", MultipleFormsLoginView.as_view()),
    path("ex_login/", ex_login),
    path("logout/", logout, name="logout"),
    path("privacy_agreement/", privacy_agree),
    path("agree_priv/", agree_pirv),
    path("register/", RegisterView.as_view()),
    path("active/<token>", user_active, name="user_active"),
    path("", include(router.urls)),
]
