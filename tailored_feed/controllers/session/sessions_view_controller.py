import inspect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from tailored_feed.services.common.log_manager import LogManager
from tailored_feed.repositories.assessment.assessment_get_repository import AssessmentGetRepository
from tailored_feed.repositories.session.session_get_repository import SessionGetRepository
from tailored_feed.services.assessment.assessment_get_service import AssessmentGetService
from tailored_feed.services.session.session_get_service import SessionGetService

log_manager = LogManager()
session_get_service = SessionGetService(SessionGetRepository())
assessment_get_service = AssessmentGetService(AssessmentGetRepository())

class SessionsViewController:

    @staticmethod
    @login_required
    def view(request, assessment_id):
        try:
            sessions = session_get_service.by_assessment_id(assessment_id)
            assessment = assessment_get_service.by_id(assessment_id)
            assessment_name = assessment.name
            
            context = {
                'assessment': {
                    'id': assessment_id,
                    'name': assessment_name
                }
            }

            return render(
                request, 
                'session/sessions_view.html', 
                {'context': context, 'sessions': sessions}
            )

        except Exception as e:
            method_name = f"{__name__}.{inspect.currentframe().f_code.co_name}"
            sig = inspect.signature(SessionsViewController.view)
            param_names = [p.name for p in sig.parameters.values() if p.kind == p.POSITIONAL_OR_KEYWORD]
            parameters = {k: v for k, v in locals().items() if k in param_names and k != 'self'}
            log_manager.log_report(method_name, parameters, str(e))
            
            return redirect('error_page')