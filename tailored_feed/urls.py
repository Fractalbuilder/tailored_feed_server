from django.urls import path
from . import views
from tailored_feed.controllers.common.error_page_controller import ErrorPageController
from tailored_feed.controllers.authentication.external_authentication_controller import LoginView, RefreshSessionView, UserView
from tailored_feed.controllers.authentication import authentication_controller
from tailored_feed.controllers.teacher_dashboard import teacher_dashboard_get_controller
from tailored_feed.controllers.assessment.assessment_dashboard_controller import AssessmentDashboardController
from tailored_feed.controllers.assessment.assessment_add_controller import AssessmentAddController
from tailored_feed.controllers.assessment.assessment_remove_controller import AssessmentRemoveController

urlpatterns = [
    path("", views.index, name="index"),
    path('error-page/', ErrorPageController.show_view, name='error_page'),
    path('login/', authentication_controller.login_view, name='login'),
    path('teacher-dashboard/', teacher_dashboard_get_controller.teacher_dashboard, name='teacher_dashboard'),
    path('external-login/', LoginView.as_view(), name='external_login'),
    path('token/refresh/', RefreshSessionView.as_view(), name='token_refresh'),
    path('user/', UserView.as_view(), name='create_user'),
    path('assessments/', AssessmentDashboardController.show_view, name='assessment_dashboard'),
    path('add-assessment/', AssessmentAddController.add, name='add_assessment'),
    path('remove-assessment/<int:assessment_id>', AssessmentRemoveController.remove, name='remove_assessment'),
]