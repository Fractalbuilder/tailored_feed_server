import inspect
import numpy as np
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.models.session.session_student import SessionStudent
from tailored_feed.models.session.session_answer import SessionAnswer
from tailored_feed.services.session_answer.session_answer_handle_service_interface import SessionAnswerHandleServiceInterface

class SessionAnswerHandleService(SessionAnswerHandleServiceInterface):

    def __init__(
        self, session_get_service, user_get_service, session_student_add_service, 
        session_answer_add_service, question_get_service, approval_sample_add_service
    ):
        self.channel_layer = get_channel_layer()
        self.exception_manager = ExceptionManager()
        self.session_get_service = session_get_service
        self.user_get_service = user_get_service
        self.session_student_add_service = session_student_add_service
        self.session_answer_add_service = session_answer_add_service
        self.question_get_service = question_get_service
        self.approval_sample_add_service = approval_sample_add_service


    def handle(
        self, question_id: int, selected_options, session_id: int, student_id: int, 
        current_question_index: int, user_context: dict, assessment_last_question_index
    ):
        try:
            is_correct = False
            session = self.session_get_service.by_id(session_id)
            student = self.user_get_service.by_id(student_id)
            question = self.question_get_service.by_index_and_assessment_id(
                current_question_index, session.assessment_id
            )
            correctAnswerIndices = question.options['correctAnswerIndices']

            if np.array_equal(selected_options, correctAnswerIndices):
                is_correct = True

            session_student = self.session_student_add_service.create_or_update_session_student(
                session, student, is_correct, current_question_index
            )

            session_answer = self.session_answer_add_service.add(
                question_id=question_id, 
                session_student=session_student, 
                question_index=question.index, 
                selected_options=selected_options,
                user_context=user_context, 
                start_date=session.startDate,
                is_correct=is_correct
            )

            prediction = self.predict_student_approval(
                session, session_student.id, current_question_index, assessment_last_question_index
            )

            if prediction:
                session_student.approvalPrediction = prediction
                session_student.save()

                self.notify_students_at_risk(session_id)

            return session_answer
            
        except Exception as e:            
            argspec = inspect.getfullargspec(self.handle)
            parameters = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "handle", parameters, str(e))


    def predict_student_approval(
        self, session, session_student_id, current_question_index, assessment_last_question_index
    ):
        if session.approvalModelQuestionIndicesAssessed:
            for i in range(len(session.approvalModelQuestionIndicesAssessed) - 1, -1, -1):
                iteration_index_assessed = session.approvalModelQuestionIndicesAssessed[i]

                if  current_question_index >= iteration_index_assessed:
                    print("Predicting...")
                    print("Index assessed")
                    print(iteration_index_assessed)
                    print("Iteration")
                    print(i)

                    print("**** HANDLE PREDICTION ****")
                    prediction = self.approval_sample_add_service.predict_student_approval(
                        session.assessment_id, session.id, session_student_id, 
                        iteration_index_assessed, i, assessment_last_question_index
                    )
                    print(prediction)
                    
                    return prediction
        
        return None


    def notify_students_at_risk(self, session_id):
        channel_layer = get_channel_layer()

        # Fetch students who are "disapproved"
        students_in_risk = (
            SessionStudent.objects
            .filter(session_id=session_id, approvalPrediction="disapproved")
            .select_related("student")  # Join with User table
            .values("id", "student__id", "student__username", "student__externalId", "correctAnswers")
            .order_by("student__externalId")
        )

        students_list = list(students_in_risk)

        # Send data to the WebSocket group
        async_to_sync(self.channel_layer.group_send)(
            f"session_{session_id}_db",
            {
                "type": "send_at_risk_students",
                "session_id": str(session_id),
                "students": students_list
            }
        )