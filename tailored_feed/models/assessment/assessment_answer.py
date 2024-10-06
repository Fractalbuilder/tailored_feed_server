from django.db import models
from django.utils.timezone import now
from tailored_feed.models.user import User
from tailored_feed.models.assessment.assessment_session import AssessmentSession

class AssessmentAnswer(models.Model):
    assessmentSession = models.ForeignKey(AssessmentSession, on_delete=models.CASCADE, related_name="answers")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answer_student")
    answer = models.IntegerField()
    creationDate = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return f"Answer {self.answer} by {self.student.username} for session {self.assessmentSession.name}"
