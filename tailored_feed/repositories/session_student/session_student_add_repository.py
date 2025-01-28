from django.db import IntegrityError
from tailored_feed.services.common.exception_manager import ExceptionManager
from django.db.models import F
from tailored_feed.models.session.session_student import SessionStudent
from tailored_feed.repositories.session_student.session_student_add_repository_interface import SessionStudentAddRepositoryInterface

class SessionStudentAddRepository(SessionStudentAddRepositoryInterface):

    def __init__(self):
        self.exception_manager = ExceptionManager()

    def create_or_update(self, session, student, approved_questions, failed_questions, current_question_index):
        """
        Creates a new SessionStudent record or updates an existing one.

        Args:
            session: The Session instance.
            student: The User (student) instance.
            approved_questions: The number of approved questions.
            failed_questions: The number of failed questions.
            current_question_index: The current question index.

        Returns:
            The created or updated SessionStudent instance.
            Returns None if there is an unexpected error during update
        Raises:
            IntegrityError: If a database integrity error occurs (e.g., unique constraint violation).
        """
        try:
            session_student, created = SessionStudent.objects.get_or_create(
                session=session,
                student=student,
                defaults={
                    'approvedQuestions': approved_questions,
                    'failedQuestions': failed_questions,
                    'currentQuestionIndex': current_question_index,
                }
            )
            
            if not created:
                # Update existing record using F expressions to avoid race conditions:
                updated_rows = SessionStudent.objects.filter(session=session, student=student).update(
                    approvedQuestions=approved_questions,
                    failedQuestions=failed_questions,
                    currentQuestionIndex=current_question_index
                )
                
                if updated_rows == 0:
                    return None # Handle the case where the record is deleted between get and update
                session_student = SessionStudent.objects.get(session=session, student=student) #refresh object

            return session_student

        except IntegrityError as e:
            raise  # Re-raise the exception after logging it, if needed.

        except SessionStudent.DoesNotExist:
            return None # Handle the case where the record is deleted between get and update
