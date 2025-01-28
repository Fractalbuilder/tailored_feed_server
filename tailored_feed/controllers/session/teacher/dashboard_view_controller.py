import inspect, redis
from django.conf import settings
from django.shortcuts import render, redirect
from tailored_feed.services.common.log_manager import LogManager
from tailored_feed.repositories.assessment.assessment_get_repository import AssessmentGetRepository
from tailored_feed.repositories.session.session_get_repository import SessionGetRepository
from tailored_feed.services.assessment.assessment_get_service import AssessmentGetService
from tailored_feed.services.session.session_get_service import SessionGetService

redis_client = redis.StrictRedis(host="127.0.0.1", port=6381, db=0)
log_manager = LogManager()
session_get_service = SessionGetService(SessionGetRepository())
assessment_get_service = AssessmentGetService(AssessmentGetRepository())

class DashboardViewController:

    @staticmethod
    def view(request, session_id, assessment_id):
        try:
            session = session_get_service.by_id(session_id)
            assessment_name = session.assessment.name
            total_questions = session.assessment.totalQuestions

            assistants_connected_key = f"session_{session.id}_assistants_connected"
            assistants_in_process_key = f"session_{session.id}_assistants_in_process"
            assistants_finished_key = f"session_{session.id}_assistants_finished"
            assistants_connected = int(redis_client.get(assistants_connected_key) or 0)
            assistants_in_process = int(redis_client.get(assistants_in_process_key) or 0)
            assistants_finished = int(redis_client.get(assistants_finished_key) or 0)

            students_developing_count = assistants_in_process
            students_finished_count = assistants_finished
            students_passed_count = 11111
            students_failed_count = 22222

            state_aliases = {
                "created": "Creada",
                "waiting": "A la espera",
                "in_process": "En desarrollo",
                "finished": "Finalizada"
            }

            backend_ip = settings.BACKEND_IP
            channels_port = settings.CHANNELS_PORT
            
            context = {
                'assessment': {
                    'id': assessment_id,
                    'name': assessment_name,
                    'total_questions': total_questions
                },
                'students': {
                    'total_count': assistants_connected,
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
                {'context': context, 'session': session, 'backend': backend_ip, 'channelsPort': channels_port}
            )

        except Exception as e:
            method_name = f"{__name__}.{inspect.currentframe().f_code.co_name}"
            sig = inspect.signature(DashboardViewController.view)
            param_names = [p.name for p in sig.parameters.values() if p.kind == p.POSITIONAL_OR_KEYWORD]
            parameters = {k: v for k, v in locals().items() if k in param_names and k != 'self'}
            log_manager.log_report(method_name, parameters, str(e))
            
            return redirect('error_page')