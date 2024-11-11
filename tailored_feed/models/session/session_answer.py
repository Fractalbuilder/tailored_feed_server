from django.db import models
from django.utils.timezone import now
from tailored_feed.models.user import User
from tailored_feed.models.assessment.assessment_question import AssessmentQuestion
from tailored_feed.models.session.session_student import SessionStudent

class SessionAnswer(models.Model):
    assessment_question = models.ForeignKey(AssessmentQuestion, on_delete=models.CASCADE, related_name="session_answer_question")
    session_student = models.ForeignKey(SessionStudent, on_delete=models.CASCADE, related_name="session_answer_student")
    optionanswered = models.IntegerField()
    creationDate = models.DateTimeField(default=now, editable=False)