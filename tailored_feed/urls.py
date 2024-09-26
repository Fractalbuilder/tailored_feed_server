from django.urls import path
from . import views
from tailored_feed.controllers.authentication.external_authentication_controller import LoginView, RefreshSessionView, UserView
from tailored_feed.controllers.authentication import authentication_controller
from tailored_feed.controllers.teacher_dashboard import teacher_dashboard_get_controller

urlpatterns = [
    path("", views.index, name="index"),
    path('login/', authentication_controller.login_view, name='login'),
    path('teacher-dashboard/', teacher_dashboard_get_controller.teacher_dashboard, name='teacher_dashboard'),
    path('external-login/', LoginView.as_view(), name='external_login'),
    path('token/refresh/', RefreshSessionView.as_view(), name='token_refresh'),
    path('user/', UserView.as_view(), name='create_user'),
]