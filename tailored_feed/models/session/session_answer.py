from django.db import models
from django.utils.timezone import now
from django.db.models import JSONField
from tailored_feed.models.user import User
from tailored_feed.models.assessment.assessment_question import AssessmentQuestion
from tailored_feed.models.session.session_student import SessionStudent

class SessionAnswer(models.Model):
    assessmentQuestion = models.ForeignKey(AssessmentQuestion, on_delete=models.CASCADE, related_name="session_answer_question")
    sessionStudent = models.ForeignKey(SessionStudent, on_delete=models.CASCADE, related_name="session_answer_student")
    selectedOptions = JSONField(default=list)
    userContext = JSONField(default=dict)
    creationDate = models.DateTimeField(default=now, editable=False)

    class Meta:
        unique_together = ('assessmentQuestion', 'sessionStudent')
        ordering = ['creationDate']