from django.urls import path
from . import session_consumer
from . import dashboard_consumer

websocket_urlpatterns = [
    path('ws/session/<str:session_id>/<str:user_id>/<int:total_questions>/', session_consumer.SessionConsumer.as_asgi()),
    path('ws/dashboard/<str:session_id>/', dashboard_consumer.DashboardConsumer.as_asgi()),
]