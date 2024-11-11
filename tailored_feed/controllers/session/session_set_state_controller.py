import inspect
from django.shortcuts import redirect
from django.contrib import messages
from tailored_feed.exceptions.content_error import ContentError
from tailored_feed.services.common.log_manager import LogManager
from tailored_feed.models.session.session import Session
from tailored_feed.repositories.session.session_get_repository import SessionGetRepository
from tailored_feed.repositories.session.session_add_repository import SessionAddRepository
from tailored_feed.services.session.session_get_service import SessionGetService
from tailored_feed.services.session.session_add_service import SessionAddService

log_manager = LogManager()
session_get_service = SessionGetService(SessionGetRepository())
session_add_service = SessionAddService(SessionAddRepository())

class SessionSetStateController:

    @staticmethod
    def set_state(request):
        try:
            if request.method != 'POST':
                raise ContentError('La petición no usa el método POST')
            
            data = request.POST
            session_id = data.get('session_id')
            new_state = data.get('new_state')
            session = session_get_service.by_id(session_id)
            
            if new_state not in [state[0] for state in Session.State.choices]:
                raise ValidationError(f"El estado '{new_state}' no es valido.")
            
            session.state = new_state

            session_add_service.add_n_save(session=session)

        except ContentError as e:
            messages.error(request, "Actualización de estado fallida. " + str(e))

        except Exception as e:
            method_name = f"{__name__}.{inspect.currentframe().f_code.co_name}"
            sig = inspect.signature(SessionSetStateController.set_state)
            param_names = [p.name for p in sig.parameters.values() if p.kind == p.POSITIONAL_OR_KEYWORD]
            parameters = {k: v for k, v in locals().items() if k in param_names and k != 'self'}
            log_manager.log_report(method_name, parameters, str(e))

            return redirect('error_page')

        return redirect(
            'dashboard_view', 
            session_id=session.id, 
            assessment_id=session.assessment.id
        )