import inspect
from django.shortcuts import redirect
from django.contrib import messages
from tailored_feed.exceptions.content_error import ContentError
from tailored_feed.services.common.log_manager import LogManager
from django.contrib.auth.decorators import login_required
from tailored_feed.models.session.session import Session
from tailored_feed.repositories.assessment.assessment_get_repository import AssessmentGetRepository
from tailored_feed.repositories.session.session_add_repository import SessionAddRepository
from tailored_feed.services.assessment.assessment_get_service import AssessmentGetService
from tailored_feed.services.session.session_add_service import SessionAddService

log_manager = LogManager()
assessment_get_service = AssessmentGetService(AssessmentGetRepository())
session_add_service = SessionAddService(SessionAddRepository())

class SessionAddController:

    @staticmethod
    @login_required
    def add(request):
        try:
            if request.method != 'POST':
                raise ContentError('La petición no usa el método POST')
            
            data = request.POST
            name = data.get('name')
            assessment_id = data.get('assessment_id')
            assessment = assessment_get_service.by_id(assessment_id)
            session = Session(name=name, assessment=assessment)
            session_add_service.add_n_save(session=session)
            messages.success(request, 'La sesión se creó exitosamente')

        except ContentError as e:
            messages.error(request, "Creación fallida. " + str(e))

        except Exception as e:
            method_name = f"{__name__}.{inspect.currentframe().f_code.co_name}"
            sig = inspect.signature(SessionAddController.add)
            param_names = [p.name for p in sig.parameters.values() if p.kind == p.POSITIONAL_OR_KEYWORD]
            parameters = {k: v for k, v in locals().items() if k in param_names and k != 'self'}
            log_manager.log_report(method_name, parameters, str(e))

            return redirect('error_page')

        return redirect('sessions_view', assessment_id=assessment_id)