import inspect
from django.db import IntegrityError
from tailored_feed.services.common.exception_manager import ExceptionManager
from tailored_feed.models.session.session_answer import SessionAnswer
from tailored_feed.services.session_student.session_student_add_service_interface import SessionStudentAddServiceInterface

class SessionStudentAddService(SessionStudentAddServiceInterface):

    def __init__(self, add_repository, get_service, session_get_service):
        self.exception_manager = ExceptionManager()
        self.add_repository = add_repository
        self.get_service = get_service
        self.session_get_service = session_get_service


    def create_or_update_session_student(
        self, session, student, is_correct, current_question_index
    ):

        """
        Service method to create or update SessionStudent.

        Args:
            session: The Session instance.
            student: The User (student) instance.
            current_question_index: The current question index.

        Returns:
            The created or updated SessionStudent instance, or None if an error occurs.
        """
        try:
            return self.add_repository.create_or_update(
                session, student, is_correct, current_question_index
            )
            
        except IntegrityError as e:
            # Handle integrity errors at the service level (e.g., logging, custom exceptions).
            print(f"IntegrityError creating/updating SessionStudent: {e}") # Example logging
            return None #Or raise a custom exception

        except Exception as e:
            print(f"Unexpected error creating/updating SessionStudent: {e}")
            return None #Or raise a custom exception


    def grade_session_students(self, session_id):
        try:
            session_students = self.get_service.by_session(session_id)
            session = self.session_get_service.by_id(session_id)
            assessment = session.assessment
            total_questions = assessment.totalQuestions

            if total_questions == 0:
                raise ValueError("Total questions cannot be zero.")

            approved_students = 0
            disapproved_students = 0
            
            for session_student in session_students:
                grade = (session_student.correctAnswers / total_questions) * 100
                session_student.grade = grade
                session_student.save()

                if grade >= 60:
                    approved_students += 1
                else:
                    disapproved_students += 1

            session.approvedStudents = approved_students
            session.disapprovedStudents = disapproved_students
            session.save()

        except Exception as e:
            argspec = inspect.getfullargspec(self.grade_session_students)
            parameters = {name: value for name, value in locals().items() if name in argspec.args and name != 'self'}
            self.exception_manager.throw_report(self, "grade_session_students", parameters, str(e))
