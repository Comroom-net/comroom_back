from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    LoginView,
    logout,
    privacy_agree,
    agree_pirv,
    RegisterView,
    user_active,
    ex_login,
    MultipleFormsLoginView,
    SchoolViewSet,
)

app_name = "school"

router = DefaultRouter()
router.register(r"api", SchoolViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("login/", MultipleFormsLoginView.as_view()),
    path("ex_login/", ex_login),
    path("logout/", logout, name="logout"),
    path("privacy_agreement/", privacy_agree),
    path("agree_priv/", agree_pirv),
    path("register/", RegisterView.as_view()),
    path("active/<token>", user_active, name="user_active"),
]
