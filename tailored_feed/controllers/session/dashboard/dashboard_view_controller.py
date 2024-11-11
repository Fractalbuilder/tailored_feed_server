import inspect
from django.shortcuts import render, redirect
from tailored_feed.services.common.log_manager import LogManager
from tailored_feed.repositories.assessment.assessment_get_repository import AssessmentGetRepository
from tailored_feed.repositories.session.session_get_repository import SessionGetRepository
from tailored_feed.services.assessment.assessment_get_service import AssessmentGetService
from tailored_feed.services.session.session_get_service import SessionGetService

log_manager = LogManager()
session_get_service = SessionGetService(SessionGetRepository())
assessment_get_service = AssessmentGetService(AssessmentGetRepository())

class DashboardViewController:

    @staticmethod
    def view(request, session_id, assessment_id):
        try:
            session = session_get_service.by_id(session_id)
            assessment_name = session.assessment.name
            students_developing_count = 8
            students_finished_count = 12
            students_passed_count = 10
            students_failed_count = 2

            state_aliases = {
                "created": "Creada",
                "waiting": "A la espera",
                "in_process": "En desarrollo",
                "finished": "Finalizada"
            }
            
            context = {
                'assessment': {
                    'id': assessment_id,
                    'name': assessment_name
                },
                'students': {
                    'total_count': students_passed_count + students_failed_count + students_developing_count,
                    'developing_count': students_developing_count,
                    'finished_count': students_finished_count,
                    'passed_count': students_passed_count,
                    'failed_count': students_failed_count
                },
                'state_aliases': state_aliases
            }

            return render(
                request, 
                'session/dashboard_view.html', 
                {'context': context, 'session': session}
            )

        except Exception as e:
            method_name = f"{__name__}.{inspect.currentframe().f_code.co_name}"
            sig = inspect.signature(DashboardViewController.view)
            param_names = [p.name for p in sig.parameters.values() if p.kind == p.POSITIONAL_OR_KEYWORD]
            parameters = {k: v for k, v in locals().items() if k in param_names and k != 'self'}
            log_manager.log_report(method_name, parameters, str(e))
            
            return redirect('error_page')