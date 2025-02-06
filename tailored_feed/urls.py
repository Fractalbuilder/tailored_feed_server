from django.urls import path
from . import views
from tailored_feed.controllers.common.error_page_view_controller import ErrorPageViewController
from tailored_feed.controllers.authentication.external_authentication_controller import LoginView, RefreshSessionView, UserView
from tailored_feed.controllers.authentication.authentication_view_controller import AuthenticationViewController
from tailored_feed.controllers.teacher import teachers_view_controller
from tailored_feed.controllers.assessment.assessments_view_controller import AssessmentsViewController
from tailored_feed.controllers.assessment.assessment_add_controller import AssessmentAddController
from tailored_feed.controllers.assessment.assessment_remove_controller import AssessmentRemoveController
from tailored_feed.controllers.question.questions_view_controller import QuestionsViewController
from tailored_feed.controllers.question.question_add_controller import QuestionAddController
from tailored_feed.controllers.question.question_remove_controller import QuestionRemoveController
from tailored_feed.controllers.question.question_update_controller import QuestionUpdateController
from tailored_feed.controllers.session.sessions_view_controller import SessionsViewController
from tailored_feed.controllers.session.session_add_controller import SessionAddController
from tailored_feed.controllers.session.session_student_add_controller import SessionStudentAddController
from tailored_feed.controllers.session.teacher.dashboard_view_controller import DashboardViewController
from tailored_feed.controllers.session.teacher.session_teacher_controller import SessionTeacherController

urlpatterns = [
    path("", views.index, name="index"),
    path('error-page/', ErrorPageViewController.view, name='error_page'),
    path('login/', AuthenticationViewController.login_view, name='login'),
    path('logout/', AuthenticationViewController.logout, name='logout'),
    path('teachers-view/', teachers_view_controller.teachers_view, name='teachers_view'),
    path('external-login/', LoginView.as_view(), name='external_login'),
    path('token/refresh/', RefreshSessionView.as_view(), name='token_refresh'),
    path('user/', UserView.as_view(), name='user_create'),
    path('assessment/', AssessmentsViewController.view, name='assessments_view'),
    path('assessment/add/', AssessmentAddController.add, name='assessment_add'),
    path('assessment/remove/', AssessmentRemoveController.remove, name='assessment_remove'),
    path('question/<int:assessment_id>', QuestionsViewController.view, name='questions_view'),
    path('question/add_view/<int:assessment_id>', QuestionAddController.view, name='question_add_view'),
    path('question/add/', QuestionAddController.add, name='question_add'),
    path('question/remove/', QuestionRemoveController.remove, name='question_remove'),
    path('question/update_view/<int:id>', QuestionUpdateController.view, name='question_update_view'),
    path('question/update/', QuestionUpdateController.update, name='question_update'),
    path('session/<int:assessment_id>', SessionsViewController.view, name='sessions_view'),
    path('session/add/', SessionAddController.add, name='session_add'),
    path('session/<int:session_id>/<int:assessment_id>', DashboardViewController.view, name='dashboard_view'),
    path('session/handle-state/', SessionTeacherController.handle_state, name='session_handle_state'),
    path('session_student/add/', SessionStudentAddController.add, name='session_student_add'),
    path('sse/sessions/', views.sse_sessions, name='sse_sessions'),   
]