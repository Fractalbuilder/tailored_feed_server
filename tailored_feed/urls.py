from django.urls import path
from . import views
from tailored_feed.controllers.common.error_page_view_controller import ErrorPageViewController
from tailored_feed.controllers.authentication.external_authentication_controller import LoginView, RefreshSessionView, UserView
from tailored_feed.controllers.authentication import authentication_controller
from tailored_feed.controllers.teacher import teachers_view_controller
from tailored_feed.controllers.assessment.assessments_view_controller import AssessmentsViewController
from tailored_feed.controllers.assessment.assessment_add_controller import AssessmentAddController
from tailored_feed.controllers.assessment.assessment_remove_controller import AssessmentRemoveController
from tailored_feed.controllers.question.questions_view_controller import QuestionsViewController
from tailored_feed.controllers.question.question_add_controller import QuestionAddController
from tailored_feed.controllers.question.question_remove_controller import QuestionRemoveController

urlpatterns = [
    path("", views.index, name="index"),
    path('error-page/', ErrorPageViewController.view, name='error_page'),
    path('login/', authentication_controller.login_view, name='login'),
    path('teachers-view/', teachers_view_controller.teachers_view, name='teachers_view'),
    path('external-login/', LoginView.as_view(), name='external_login'),
    path('token/refresh/', RefreshSessionView.as_view(), name='token_refresh'),
    path('user/', UserView.as_view(), name='user_create'),
    path('assessment/', AssessmentsViewController.view, name='assessments_view'),
    path('assessment/add/', AssessmentAddController.add, name='assessment_add'),
    path('assessment/remove/', AssessmentRemoveController.remove, name='assessment_remove'),
    path('question/<int:assessment_id>', QuestionsViewController.view, name='questions_view'),
    path('question/add_view/<int:assessment_id>', QuestionAddController.question_add_view, name='question_add_view'),
    path('question/add/', QuestionAddController.add, name='question_add'),
    path('question/remove/', QuestionRemoveController.remove, name='question_remove'),
]