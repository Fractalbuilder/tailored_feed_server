from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
import json, redis

redis_client = redis.StrictRedis(host="127.0.0.1", port=6381, db=0)

class SessionConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        from tailored_feed.repositories.session.session_get_repository import SessionGetRepository
        from tailored_feed.repositories.user.user_get_repository import UserGetRepository
        from tailored_feed.repositories.session_student.session_student_get_repository import SessionStudentGetRepository
        from tailored_feed.services.session.session_get_service import SessionGetService
        from tailored_feed.services.user.user_get_service import UserGetService
        from tailored_feed.services.session_student.session_student_get_service import SessionStudentGetService
        from tailored_feed.repositories.session_student.session_student_get_repository import SessionStudentGetRepository

        session_get_service = SessionGetService(SessionGetRepository())
        user_get_service = UserGetService(UserGetRepository())
        session_student_get_service = SessionStudentGetService(SessionStudentGetRepository(), session_get_service, user_get_service)
        
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.total_questions = self.scope['url_route']['kwargs']['total_questions']
        self.group_name = f"session_{self.session_id}"
        self.group_name_db = f"session_{self.session_id}_db"
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        assistants_connected = await self.increment_assistants_connected(self.session_id)

        await self.dashboard_notify_connected(assistants_connected)
        await self.accept()

        question_index = await self.get_current_question_index(session_student_get_service, self.session_id, self.user_id)
        await self.handle_response_signal(question_index)
        

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        
        assistants_connected = await self.decrement_assistants_connected(self.session_id)
        await self.dashboard_notify_connected(assistants_connected)


    async def receive(self, text_data):

        from tailored_feed.repositories.session.session_get_repository import SessionGetRepository
        from tailored_feed.repositories.user.user_get_repository import UserGetRepository
        from tailored_feed.repositories.question.question_get_repository import QuestionGetRepository
        from tailored_feed.repositories.session_student.session_student_add_repository import SessionStudentAddRepository
        from tailored_feed.repositories.session_answer.session_answer_add_repository import SessionAnswerAddRepository
        from tailored_feed.services.session.session_get_service import SessionGetService
        from tailored_feed.services.user.user_get_service import UserGetService
        from tailored_feed.services.question.question_get_service import QuestionGetService
        from tailored_feed.services.session_student.session_student_add_service import SessionStudentAddService
        from tailored_feed.services.session_answer.session_answer_add_service import SessionAnswerAddService
        from tailored_feed.services.session_answer.session_answer_handle_service import SessionAnswerHandleService

        session_get_service = SessionGetService(SessionGetRepository())
        user_get_service = UserGetService(UserGetRepository())
        question_get_service = QuestionGetService(QuestionGetRepository())
        session_student_add_service = SessionStudentAddService(SessionStudentAddRepository())
        session_answer_add_service = SessionAnswerAddService(SessionAnswerAddRepository(), question_get_service)
        session_answer_handle_service = SessionAnswerHandleService(session_get_service, user_get_service, session_student_add_service, session_answer_add_service)

        try:
            data = json.loads(text_data)
            message_type = data.get('type')

            if message_type == 'answer':
                payload = data.get('payload')
                user_id = payload.get('userId')
                session_id = payload.get('sessionId')
                question_id = payload.get('questionId')
                question_index = payload.get('questionIndex')
                selected_options_indices = payload.get('selectedOptionsIndices')
                total_questions = payload.get('totalQuestions')
                print(f"Session ID: {session_id}. User ID: {user_id}. Question ID: {question_id}. Question index: {question_index}. Selected options: {selected_options_indices}. Total questions: {total_questions}.")
                
                await self.handle_answer(
                    session_answer_handle_service, question_id, selected_options_indices, 
                    session_id, user_id, 0, 0, question_index
                )
                
                await self.handle_response_signal(question_index)

            else:
                print(f"Received unknown message type: {message_type}")

        except json.JSONDecodeError:
            print(f"Invalid JSON received: {text_data}")

        except Exception as e:
            print(f"Error processing message: {e}")


    async def handle_response_signal(self, current_question_index):

        from tailored_feed.repositories.session.session_get_repository import SessionGetRepository
        from tailored_feed.services.session.session_get_service import SessionGetService

        session_get_service = SessionGetService(SessionGetRepository())
        
        session = await self.get_session(session_get_service, self.session_id)
        
        if session is None:
            raise Exception(f'No se encontró la sesión con ID {session_id}.')

        if session.state == "waiting":
            event = {
                "message": "La sesión de evaluación aún no ha iniciado",
                "code": 0
            }

            await self.send_notification_signal(event)

        elif session.state == "in_process":
            next_question_index = current_question_index + 1
            
            if next_question_index < self.total_questions:
                await self.handle_question(session.assessment_id, next_question_index)
                
            else:
                event = {
                    "message": "La sesión de evaluación se ha completado",
                    "code": 1
                }

                await self.send_notification_signal(event)
                assistants_in_process_key = f"session_{session.id}_assistants_in_process"
                assistants_finished_key = f"session_{session.id}_assistants_finished"
                redis_client.decr(assistants_in_process_key)
                redis_client.incr(assistants_finished_key)
                assistants_in_process = int(redis_client.get(assistants_in_process_key))
                assistants_finished = int(redis_client.get(assistants_finished_key))
                await self.dashboard_notify_completeness(assistants_in_process, assistants_finished)

        else:
            event = {
                "message": "La sesión de evaluación ha terminado",
                "code": 1
            }

            await self.send_notification_signal(event)


    async def handle_question(self, assessment_id, index):
        from tailored_feed.repositories.question.question_get_repository import QuestionGetRepository
        from tailored_feed.services.question.question_get_service import QuestionGetService

        question_get_service = QuestionGetService(QuestionGetRepository())

        raw_question = await self.get_question_by_index_and_assessment_id(question_get_service, index, assessment_id)

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

        signal = {
            "type": "question",
            "question": question,
            "feedback": None
        }

        await self.send(text_data=json.dumps(signal))


    @staticmethod
    async def increment_assistants_connected(session_id):
        assistants_connected_key = f"session_{session_id}_assistants_connected"
        redis_client.incr(assistants_connected_key)
        return int(redis_client.get(assistants_connected_key))


    @staticmethod
    async def decrement_assistants_connected(session_id):
        assistants_connected_key = f"session_{session_id}_assistants_connected"
        redis_client.decr(assistants_connected_key)
        return int(redis_client.get(assistants_connected_key))


    async def dashboard_notify_connected(self, assistants_connected):
        await self.channel_layer.group_send(
            self.group_name_db,
            {
                "type": "update_connected",
                "session_id": self.session_id,
                "assistants_connected": assistants_connected,
            }
        )

    
    async def dashboard_notify_completeness(self, assistants_in_process, assistants_finished):
        await self.channel_layer.group_send(
            self.group_name_db,
            {
                "type": "update_completeness",
                "session_id": self.session_id,
                "assistants_in_process": assistants_in_process,
                "assistants_finished": assistants_finished,
            }
        )


    async def send_question(self, event):
        signal = {
            "type": event['message_type'],
            "question": event['question'],
            "feedback": event['feedback']
        }

        await self.send(text_data=json.dumps(signal))


    async def send_notification_signal(self, event):
        signal = {
            "type": "notification",
            "message": event['message'],
            "code": event['code'],
        }

        await self.send(text_data=json.dumps(signal))


    @database_sync_to_async
    def get_session(self, session_get_service, session_id):
        return session_get_service.by_id(session_id)


    @database_sync_to_async
    def get_question_by_index_and_assessment_id(self, question_get_service, index, assessment_id):
        return question_get_service.by_index_and_assessment_id(index, assessment_id)


    @database_sync_to_async
    def handle_answer(
        self, session_answer_handle_service, question_id, selected_options_indices, 
        session_id, user_id, approved_questions, failed_questions, question_index
    ):  
        return session_answer_handle_service.handle(
            question_id=question_id, selected_options=selected_options_indices, 
            session_id=session_id, student_id=user_id, approved_questions=approved_questions, 
            failed_questions=failed_questions, current_question_index=question_index
        )


    @database_sync_to_async
    def get_total_questions(self, assessment_get_service, assessment_id):
        return assessement_get_service.by_id(assessment_id).totalQuestions


    @database_sync_to_async
    def get_current_question_index(self, session_student_get_service, session_id, student_id):
        return session_student_get_service.by_session_n_user(session_id, student_id).currentQuestionIndex