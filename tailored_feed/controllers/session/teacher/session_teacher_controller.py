import inspect
from django.shortcuts import render, redirect
from django.http import JsonResponse
from tailored_feed.services.common.log_manager import LogManager
from tailored_feed.repositories.session.session_add_repository import SessionAddRepository
from tailored_feed.repositories.session.session_get_repository import SessionGetRepository
from tailored_feed.repositories.question.question_get_repository import QuestionGetRepository
from tailored_feed.services.session.session_add_service import SessionAddService
from tailored_feed.services.session.session_get_service import SessionGetService
from tailored_feed.services.question.question_get_service import QuestionGetService
from tailored_feed.services.session.teacher.session_teacher_service import SessionTeacherService

log_manager = LogManager()
session_add_service = SessionAddService(SessionAddRepository())
session_get_service = SessionGetService(SessionGetRepository())
question_get_service = QuestionGetService(QuestionGetRepository())
session_teacher_service = SessionTeacherService(
    session_add_service, session_get_service, question_get_service
    )

class SessionTeacherController:

    @staticmethod
    def handle_state(request):
        try:
            data = request.POST
            session_id = data.get('session_id')
            new_state = data.get('new_state')
            assessment_id = data.get('assessment_id')
            session_teacher_service.handle_state(session_id=session_id, new_state=new_state)
            
            return redirect(
                'dashboard_view', 
                session_id=session_id, 
                assessment_id=assessment_id
            )

        except Exception as e:
            method_name = f"{__name__}.{inspect.currentframe().f_code.co_name}"
            sig = inspect.signature(SessionTeacherController.handle_state)
            param_names = [p.name for p in sig.parameters.values() if p.kind == p.POSITIONAL_OR_KEYWORD]
            parameters = {k: v for k, v in locals().items() if k in param_names and k != 'self'}
            log_manager.log_report(method_name, parameters, str(e))
        
        return redirect('error_page')