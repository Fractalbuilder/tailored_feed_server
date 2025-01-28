import inspect, redis
from tailored_feed.services.common.exception_manager import ExceptionManager
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from tailored_feed.models.session.session import Session
from tailored_feed.repositories.session.session_get_repository import SessionGetRepository
from tailored_feed.services.session.session_get_service import SessionGetService
from tailored_feed.services.session.teacher.session_teacher_service_interface import SessionTeacherServiceInterface

redis_client = redis.StrictRedis(host="127.0.0.1", port=6381, db=0)

class SessionTeacherService(SessionTeacherServiceInterface):
    
    def __init__(self, session_add_service, session_get_service, question_get_service):
        self.exception_manager = ExceptionManager()
        self.channel_layer = get_channel_layer()
        self.session_add_service = session_add_service
        self.session_get_service = session_get_service
        self.question_get_service = question_get_service


    def handle_state(self, session_id, new_state):
        try:
            session = self.session_get_service.by_id(session_id)
            
            if new_state not in [state[0] for state in Session.State.choices]:
                raise ValidationError(f"El estado '{new_state}' no es valido.")
            
            session.state = new_state
            session = self.session_add_service.add_n_save(session=session)
            assistants_connected_key = f"session_{session.id}_assistants_connected"
            print("Handle")
            print(assistants_connected_key)
            assistants_in_process_key = f"session_{session.id}_assistants_in_process_key"
            assistants_finished_key = f"session_{session.id}_assistants_finished"

            if new_state == "waiting":
                redis_client.set(assistants_connected_key, 0)
                redis_client.set(assistants_in_process_key, 0)
                redis_client.set(assistants_finished_key, 0)
            
            elif new_state == "in_process":
                assistants_connected = int(redis_client.get(assistants_connected_key))
                assistants_in_process_key = f"session_{session.id}_assistants_in_process"
                redis_client.set(assistants_in_process_key, assistants_connected)
                self.start_session(session_id, session.assessment.id)
            
            elif new_state == "finished":
                self.end_session(session_id)
            
        except Exception as e:
            argspec = inspect.getfullargspec(self.handle_state)
            parameters = {name: value for name, value in locals().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "handle_state", parameters, str(e))


    def start_session(self, session_id, assessment_id):
        try:
            group_name = f"session_{session_id}"
            raw_question = self.question_get_service.by_index_and_assessment_id(0, assessment_id)

            if raw_question is None:
                raise Exception(f'No se encontró la pregunta con ID {assessment_id}.')

            question_options = raw_question.options
            options = []

            for question_option in question_options:
                options.append(question_option['statement'])

            feedback = None
            
            if raw_question.feedback_image:
                feedback = {
                    "type": "image",
                    "data": raw_question.feedback_image.url
                }
            elif raw_question.feedback_text:
                feedback = {
                    "type": "text",
                    "data": raw_question.feedback_text
                }
            
            question = {
                "id": raw_question.id,
                "statement": raw_question.statement,
                "options": options,
                "index": raw_question.index,
                "feedback": feedback
            }
            
            async_to_sync(self.channel_layer.group_send)(
                group_name,
                {
                    "type": "send_question",
                    "message_type": "question",
                    "question": question,
                    "feedback": None
                }
            )

        except Exception as e:
            argspec = inspect.getfullargspec(self.start_session)
            parameters = {name: value for name, value in locals().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "start_session", parameters, str(e))


    def end_session(self, session_id):
        try:
            group_name = f"session_{session_id}"
            async_to_sync(self.channel_layer.group_send)(
                group_name,
                {
                    "type": "send_notification_signal",
                    "message": "La sesión de evaluación ha terminado",
                    "code": 1
                }
            )

        except Exception as e:
            argspec = inspect.getfullargspec(self.end_session)
            parameters = {name: value for name, value in locals().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "end_session", parameters, str(e))