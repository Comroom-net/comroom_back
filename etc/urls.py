from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    NoticeNocookieViewSet,
    DisabledChannelViewSet,
    nocookie,
    GsuiteConvertor,
    load_html,
    load_last_html,
)

app_name = "etc"

router = DefaultRouter()
router.register(r"nocookie", NoticeNocookieViewSet)
router.register(r"disabled-ch", DisabledChannelViewSet)

urlpatterns = [
    path("nocookie", nocookie, name="nocookie"),
    path("g-suite", GsuiteConvertor, name="GsuiteConvertor"),
    path("page", load_last_html, name="page"),
    path("page/<int:pk>", load_html, name="page"),
    path("", include(router.urls)),
]
