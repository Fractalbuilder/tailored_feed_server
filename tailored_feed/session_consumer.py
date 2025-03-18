import json, redis, random
from datetime import timedelta, datetime
from django.utils.timezone import now
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async

redis_client = redis.StrictRedis(host="127.0.0.1", port=6381, db=0)

class SessionConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        from tailored_feed.repositories.session.session_get_repository import SessionGetRepository
        from tailored_feed.repositories.user.user_get_repository import UserGetRepository
        from tailored_feed.repositories.session_student.session_student_get_repository import SessionStudentGetRepository
        from tailored_feed.repositories.session_student.session_student_add_repository import SessionStudentAddRepository
        from tailored_feed.services.session.session_get_service import SessionGetService
        from tailored_feed.services.user.user_get_service import UserGetService
        from tailored_feed.services.session_student.session_student_get_service import SessionStudentGetService
        from tailored_feed.services.session_student.session_student_add_service import SessionStudentAddService
        from tailored_feed.repositories.session_student.session_student_get_repository import SessionStudentGetRepository

        session_get_service = SessionGetService(SessionGetRepository())
        user_get_service = UserGetService(UserGetRepository())
        session_student_get_service = SessionStudentGetService(
            SessionStudentGetRepository(), session_get_service, user_get_service
        )

        session_student_add_service = SessionStudentAddService(
            SessionStudentAddRepository(), session_student_get_service, session_get_service
        )
        
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.total_questions = self.scope['url_route']['kwargs']['total_questions']
        self.duration = self.scope['url_route']['kwargs']['duration']
        self.group_name = f"session_{self.session_id}"
        self.group_name_db = f"session_{self.session_id}_db"
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        assistants_connected = await self.increment_assistants_connected(self.session_id)

        await self.dashboard_notify_connected(assistants_connected)
        await self.accept()

        session_student = await self.get_session_student(session_student_get_service)
        self.session_student_id = session_student.id
        question_index = session_student.currentQuestionIndex

        await self.handle_response_signal(
            question_index, session_student_get_service, session_student_add_service
        )
        
        
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
        from tailored_feed.repositories.session_student.session_student_get_repository import SessionStudentGetRepository
        from tailored_feed.repositories.session_student.session_student_add_repository import SessionStudentAddRepository
        from tailored_feed.repositories.session_answer.session_answer_add_repository import SessionAnswerAddRepository
        from tailored_feed.repositories.user.user_get_repository import UserGetRepository
        from tailored_feed.repositories.ai.approval_sample_get_repository import ApprovalSampleGetRepository
        from tailored_feed.repositories.ai.approval_sample_add_repository import ApprovalSampleAddRepository
        from tailored_feed.services.session.session_get_service import SessionGetService
        from tailored_feed.services.user.user_get_service import UserGetService
        from tailored_feed.services.question.question_get_service import QuestionGetService
        from tailored_feed.services.session_student.session_student_get_service import SessionStudentGetService
        from tailored_feed.services.session_student.session_student_add_service import SessionStudentAddService
        from tailored_feed.services.session_answer.session_answer_add_service import SessionAnswerAddService
        from tailored_feed.services.session_answer.session_answer_handle_service import SessionAnswerHandleService
        from tailored_feed.services.ai.approval_sample_add_service import ApprovalSampleAddService

        session_get_service = SessionGetService(SessionGetRepository())
        user_get_service = UserGetService(UserGetRepository())
        question_get_service = QuestionGetService(QuestionGetRepository())
        session_student_get_service = SessionStudentGetService(
            SessionStudentGetRepository(), session_get_service, UserGetRepository()
        )

        session_student_add_service = SessionStudentAddService(
            SessionStudentAddRepository(), session_student_get_service, session_get_service
        )

        session_answer_add_service = SessionAnswerAddService(SessionAnswerAddRepository(), question_get_service)
        
        approval_sample_add_service = ApprovalSampleAddService(
            ApprovalSampleGetRepository(), ApprovalSampleAddRepository()
        )

        session_answer_handle_service = SessionAnswerHandleService(
            session_get_service, user_get_service, session_student_add_service, 
            session_answer_add_service, question_get_service, approval_sample_add_service
        )

        try:
            data = json.loads(text_data)
            message_type = data.get('type')

            if message_type == 'answer':
                payload = data.get('payload')
                user_id = payload.get('userId')
                session_id = payload.get('sessionId')
                question_id = payload.get('questionId')
                selected_options_indices = payload.get('selectedOptionsIndices')
                question_index = payload.get('questionIndex')
                user_context = payload.get('userContext')

                # TMP correction
                if user_context["bandwidth"] == 0:
                    user_context["bandwidth"] = 20.0123456789
                    print("Bandwidth corrected")

                #print(f"Session ID: {session_id}. User ID: {user_id}. Question ID: {question_id}. Question index: {question_index}. Selected options: {selected_options_indices}. Total questions: {self.total_questions}.")
                #print(f"User context: {user_context}")

                await self.handle_answer(
                    session_answer_handle_service, question_id, selected_options_indices, 
                    session_id, user_id, question_index, user_context
                )
                
                await self.handle_response_signal(
                    question_index, session_student_get_service, session_student_add_service
                )
                
            else:
                print(f"Received unknown message type: {message_type}")

        except json.JSONDecodeError:
            print(f"Invalid JSON received: {text_data}")

        except Exception as e:
            print(f"Error processing message: {e}")


    async def handle_response_signal(
        self, current_question_index, session_student_get_service, session_student_add_service
    ):

        from tailored_feed.repositories.session.session_get_repository import SessionGetRepository
        from tailored_feed.services.session.session_get_service import SessionGetService
        from tailored_feed.repositories.session.session_add_repository import SessionAddRepository
        from tailored_feed.repositories.ai.approval_sample_get_repository import ApprovalSampleGetRepository
        from tailored_feed.repositories.ai.approval_sample_add_repository import ApprovalSampleAddRepository
        from tailored_feed.services.session.session_add_service import SessionAddService
        from tailored_feed.services.ai.approval_sample_add_service import ApprovalSampleAddService

        session_get_service = SessionGetService(SessionGetRepository())
        session_add_service = SessionAddService(SessionAddRepository())
        approval_sample_add_service = ApprovalSampleAddService(
            ApprovalSampleGetRepository(), ApprovalSampleAddRepository()
        )

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
                await self.handle_question(
                    session_student_get_service, session, next_question_index
                )
                
            else:
                event = {
                    "message": "La sesión de evaluación se ha completado",
                    "code": 1
                }

                await self.grade_student(session_student_add_service)
                await self.send_notification_signal(event)
                assistants_in_process_key = f"session_{session.id}_assistants_in_process"
                assistants_finished_key = f"session_{session.id}_assistants_finished"
                redis_client.decr(assistants_in_process_key)
                redis_client.incr(assistants_finished_key)
                assistants_in_process = int(redis_client.get(assistants_in_process_key))
                assistants_finished = int(redis_client.get(assistants_finished_key))
                session.finishedStudents = session.finishedStudents + 1
                session = await self.add_session(session_add_service, session)

                await self.dashboard_notify_completeness(assistants_in_process, assistants_finished)
                
                approval_model_iteration_index = self.get_approval_model_iteration_index(
                    session.enrolledStudents, session.finishedStudents
                )
                print("approval_model_iteration_index: ")
                print(approval_model_iteration_index)
                if approval_model_iteration_index != -1:
                    """
                    avg_question_index = await self.get_avg_question_index(
                        session_student_get_service
                    )
                    print('avg_question_index: ')
                    print(avg_question_index)
                    """
                    question_index_assessed = self.get_approval_model_question_index_assessed(approval_model_iteration_index)

                    if question_index_assessed != -1:
                        await self.approval_sample_generate_iteration_model(
                            approval_sample_add_service,
                            approval_model_iteration_index, 
                            session.assessment_id, 
                            question_index_assessed
                        )

        else:
            event = {
                "message": "La sesión de evaluación ha terminado",
                "code": 1
            }

            await self.send_notification_signal(event)


    async def handle_question(self, session_student_get_service, session, index):
        
        from tailored_feed.repositories.question.question_get_repository import QuestionGetRepository
        from tailored_feed.services.question.question_get_service import QuestionGetService

        question_get_service = QuestionGetService(QuestionGetRepository())

        assessment_id = session.assessment_id
        feedback_enabled = session.feedbackEnabled
        raw_question = await self.get_question_by_index_and_assessment_id(question_get_service, index, assessment_id)

        if raw_question is None:
            raise Exception(f'No se encontró la pregunta con ID {assessment_id}.')

        question_options = raw_question.options['options']
        options = []

        for question_option in question_options:
            options.append(question_option['statement'])
        
        session_student = await self.get_session_student(session_student_get_service)
        feedback = await self.get_feedback(
            question_get_service, session_student.approvalPrediction, index, assessment_id, feedback_enabled, session
        )
        
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


    async def get_feedback(
        self, question_get_service, approvalPrediction, index, assessment_id, feedback_enabled, session
    ):
        feedback = None
        
        if (feedback_enabled and index > 0):
            if(approvalPrediction == "not_predicted" or approvalPrediction == "disapproved"):
                feedback = await self.get_hint_feedback(question_get_service, index, assessment_id)

                if feedback:
                    return feedback
            
            feedback = self.get_session_feedback(session, index)

        return feedback


    async def get_hint_feedback(self, question_get_service, index, assessment_id):
        feedback = None
        raw_previous_question = await self.get_question_by_index_and_assessment_id(
            question_get_service, index - 1, assessment_id
        )
        
        if raw_previous_question.feedback_image:
            feedback = {
                "type": "image",
                "data": raw_previous_question.feedback_image.url
            }
        elif raw_previous_question.feedback_text:
            feedback = {
                "type": "text",
                "data": raw_previous_question.feedback_text
            }

        return feedback


    def get_approval_model_iteration_index(self, enrolled_students, finished_students):
        partitions = 4
        students_in_partition = enrolled_students//partitions

        if students_in_partition > 0:
            for i in range(1, partitions):
                finished_students_in_iteration = students_in_partition * i
                
                if finished_students_in_iteration == finished_students:
                    return i - 1

        return -1


    def get_approval_model_question_index_assessed(self, approval_model_iteration_index):
        if approval_model_iteration_index < 0 or approval_model_iteration_index > 2:
            raise Exception(f"El valor de approval_model_iteration_index '{approval_model_iteration_index}' no es valido, solo se admiten los valores 0, 1 y 2, correspondientes a las iteraciones en que se genera un modelo de predicción.")
        
        partitions = 4
        questions_in_partition = self.total_questions//partitions

        if questions_in_partition > 0:
            for i in range(1, partitions):
                index_assessed = (questions_in_partition * i) - 1
                
                if (i-1) == approval_model_iteration_index:
                    return index_assessed

        return -1


    def get_session_feedback(self, session, index):
        random_value = random.randint(0, 1)

        if random_value:
            return {
                "type": "text",
                "data": f"Preguntas respondidas: {index}\nPregunta pendientes: {self.total_questions - index}"
            }

        else:
            elapsed_time = int((now() - session.startDate).total_seconds() / 60)
            end_time = session.startDate + timedelta(minutes=self.duration)
            remaining_time = int((end_time - now()).total_seconds() / 60)

            return {
                "type": "text",
                "data": f"Tiempo transcurrido: {elapsed_time} min\nTiempo restante: {remaining_time} min"
            }


    @database_sync_to_async
    def get_session(self, session_get_service, session_id):
        return session_get_service.by_id(session_id)


    @database_sync_to_async
    def add_session(self, session_add_service, session):
        return session_add_service.add_n_save(session)


    @database_sync_to_async
    def get_question_by_index_and_assessment_id(self, question_get_service, index, assessment_id):
        return question_get_service.by_index_and_assessment_id(index, assessment_id)


    @database_sync_to_async
    def handle_answer(
        self, session_answer_handle_service, question_id, selected_options_indices, 
        session_id, user_id, question_index, user_context
    ):  
        return session_answer_handle_service.handle(
            question_id=question_id, selected_options=selected_options_indices, 
            session_id=session_id, student_id=user_id, current_question_index=question_index,
            user_context=user_context, assessment_last_question_index=self.total_questions - 1
        )

    
    @database_sync_to_async
    def get_session_student(self, session_student_get_service):
        return session_student_get_service.by_session_n_user(self.session_id, self.user_id)

    """
    Deprecated
    @database_sync_to_async
    def get_avg_question_index(self, session_student_get_service):
        return session_student_get_service.get_avg_question_index(
            self.session_id, self.total_questions - 1
        )
    """

    @database_sync_to_async
    def grade_student(self, session_student_add_service):
        session_student_add_service.grade_student(self.session_id, self.user_id, self.total_questions)


    @database_sync_to_async
    def approval_sample_generate_iteration_model(
        self, approval_sample_add_service, iteration, 
        assessment_id, question_index_assessed
    ):
        return approval_sample_add_service.generate_iteration_model(
            iteration, assessment_id, self.session_student_id, self.session_id, 
            question_index_assessed, self.total_questions - 1
        )