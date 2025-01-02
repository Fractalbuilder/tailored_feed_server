import inspect
from django.shortcuts import redirect
from django.contrib import messages
from tailored_feed.exceptions.content_error import ContentError
from tailored_feed.services.common.log_manager import LogManager
from tailored_feed.models.session.session import Session
from tailored_feed.repositories.assessment.assessment_get_repository import AssessmentGetRepository
from tailored_feed.repositories.session.session_add_repository import SessionAddRepository
from tailored_feed.services.assessment.assessment_get_service import AssessmentGetService
from tailored_feed.services.session.session_add_service import SessionAddService

log_manager = LogManager()
assessment_get_service = AssessmentGetService(AssessmentGetRepository())
session_add_service = SessionAddService(SessionAddRepository())

class SessionStudentAddController:

    @staticmethod
    def add(request):
        try:
            if request.method != 'POST':
                raise ContentError('La petición no usa el método POST')
            
            data = request.POST
            session_id = data.get('session_id')
            student_id = data.get('student_id')
            session_student_add_service.add_n_save(session_id=session_id, student_id=student_id)
            messages.success(request, 'El estudiante se vinculó a la sesión exitosamente')

        except ContentError as e:
            messages.error(request, "Agregación fallida. " + str(e))

        except Exception as e:
            method_name = f"{__name__}.{inspect.currentframe().f_code.co_name}"
            sig = inspect.signature(SessionStudentAddController.add)
            param_names = [p.name for p in sig.parameters.values() if p.kind == p.POSITIONAL_OR_KEYWORD]
            parameters = {k: v for k, v in locals().items() if k in param_names and k != 'self'}
            log_manager.log_report(method_name, parameters, str(e))

            return redirect('error_page')