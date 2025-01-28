import inspect
from django.db import IntegrityError
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.models.session.session_answer import SessionAnswer
from tailored_feed.services.session_student.session_student_add_service_interface import SessionStudentAddServiceInterface

class SessionStudentAddService(SessionStudentAddServiceInterface):

    def __init__(self, add_repository):
        self.exception_manager = ExceptionManager()
        self.add_repository = add_repository


    def create_or_update_session_student(self, session, student, approved_questions, failed_questions, current_question_index):

        """
        Service method to create or update SessionStudent.

        Args:
            session: The Session instance.
            student: The User (student) instance.
            approved_questions: The number of approved questions.
            failed_questions: The number of failed questions.
            current_question_index: The current question index.

        Returns:
            The created or updated SessionStudent instance, or None if an error occurs.
        """
        try:
            return self.add_repository.create_or_update(session, student, approved_questions, failed_questions, current_question_index)
            
        except IntegrityError as e:
            # Handle integrity errors at the service level (e.g., logging, custom exceptions).
            print(f"IntegrityError creating/updating SessionStudent: {e}") # Example logging
            return None #Or raise a custom exception

        except Exception as e:
            print(f"Unexpected error creating/updating SessionStudent: {e}")
            return None #Or raise a custom exception