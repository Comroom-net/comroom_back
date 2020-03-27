from django.urls import path

from .views import LoginView, logout, privacy_agree, agree_pirv, RegisterView, user_active, ex_login,\
    MultipleFormsLoginView

app_name = 'school'
urlpatterns = [
    # path('login/', LoginView.as_view()),
    path('login/', MultipleFormsLoginView.as_view()),
    path('ex_login/', ex_login),
    path('logout/', logout, name='logout'),
    path('privacy_agreement/', privacy_agree),
    path('agree_priv/', agree_pirv),
    path('register/', RegisterView.as_view()),
    path('active/<token>', user_active, name='user_active'),
]
