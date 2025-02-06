from django.db import IntegrityError
from tailored_feed.services.common.exception_manager import ExceptionManager
from django.db.models import F
from tailored_feed.models.session.session_student import SessionStudent
from tailored_feed.repositories.session_student.session_student_add_repository_interface import SessionStudentAddRepositoryInterface

class SessionStudentAddRepository(SessionStudentAddRepositoryInterface):

    def __init__(self):
        self.exception_manager = ExceptionManager()

    def create_or_update(
        self, session, student, is_correct, current_question_index
    ):
        """
        Creates a new SessionStudent record or updates an existing one.

        Args:
            session: The Session instance.
            student: The User (student) instance.
            is_correct: Boolean indicating whether the answer is correct (True) or wrong (False).
            current_question_index: The current question index.

        Returns:
            The created or updated SessionStudent instance.
            Returns None if there is an unexpected error during update.
        Raises:
            IntegrityError: If a database integrity error occurs (e.g., unique constraint violation).
        """
        try:
            session_student, created = SessionStudent.objects.get_or_create(
                session=session,
                student=student,
                defaults={
                    'correctAnswers': 1 if is_correct else 0,
                    'wrongAnswers': 0 if is_correct else 1,
                    'currentQuestionIndex': current_question_index,
                }
            )

            if not created:
                # Increment the correctAnswers or wrongAnswers field accordingly
                update_fields = {
                    'correctAnswers': F('correctAnswers') + 1
                } if is_correct else {
                    'wrongAnswers': F('wrongAnswers') + 1
                }
                update_fields['currentQuestionIndex'] = current_question_index

                updated_rows = SessionStudent.objects.filter(session=session, student=student).update(**update_fields)

                if updated_rows == 0:
                    return None  # Handle the case where the record is deleted between get and update
                session_student.refresh_from_db()

            return session_student

        except IntegrityError as e:
            raise  # Re-raise the exception after logging it, if needed.

        except SessionStudent.DoesNotExist:
            return None  # Handle the case where the record is deleted between get and update
