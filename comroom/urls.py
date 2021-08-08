from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )


from school.views import (
    index,
    AboutView,
    ComroomAdminView,
    make_room,
    reset_password,
    send_password_mail,
    token_signin,
)
from timetable.views import assign_room

urlpatterns = [
    path("tokensignin", token_signin),
    path("admin/", admin.site.urls),
    # path("accounts/", include("allauth.urls")),
    path("", index, name="index"),
    # path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("school/", include("school.urls")),
    path("etc/", include("etc.urls")),
    path("afterschool/", include("afterschool.urls")),
    path("namu/", include("namu.urls")),
    # path('make_room/', make_room),
    # path('assign_room/', assign_room),
    path("send_password_mail/", send_password_mail, name="send_password_mail"),
    path("reset_password/<str:token>/", reset_password),
    path("comroom_admin/", ComroomAdminView.as_view()),
    path("ssam_ko/", AboutView.as_view(), name="about"),
    path("howto/", TemplateView.as_view(template_name="howto.html")),
    path("whatis/", TemplateView.as_view(template_name="whatis.html")),
    path("FAQ/", TemplateView.as_view(template_name="faq.html")),
    path("db_reset/", TemplateView.as_view(template_name="dbreset.html")),
    path("timetable/", include("timetable.urls", namespace="timetable")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    # path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
