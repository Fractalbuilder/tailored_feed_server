from django.urls import path
from . import views
from tailored_feed.controllers.common.authentication_controller import LoginView, RefreshSessionView, UserView

urlpatterns = [
    path("", views.index, name="index"),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', RefreshSessionView.as_view(), name='token_refresh'),
    path('user/', UserView.as_view(), name='create_user'),
]