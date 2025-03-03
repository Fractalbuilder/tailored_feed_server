from django.db import models
from django.utils.timezone import now
from django.utils import timezone
from django.db.models import JSONField
from tailored_feed.models.assessment.assessment_question import AssessmentQuestion
from tailored_feed.models.session.session_student import SessionStudent

class SessionAnswer(models.Model):
    assessmentQuestion = models.ForeignKey(AssessmentQuestion, on_delete=models.CASCADE, related_name="session_answer_question")
    sessionStudent = models.ForeignKey(SessionStudent, on_delete=models.CASCADE, related_name="session_answer_student")
    questionIndex = models.IntegerField()
    selectedOptions = JSONField(default=list)
    userContext = JSONField(default=dict)
    creationDate = models.DateTimeField(default=now, editable=False)
    elapsedTime = models.IntegerField()
    isCorrect = models.BooleanField()

    class Meta:
        unique_together = ('assessmentQuestion', 'sessionStudent')
        ordering = ['creationDate']

    def to_dict(self):
        return {
            "assessmentQuestion": self.assessmentQuestion_id if self.assessmentQuestion else None,  # Or self.assessmentQuestion if you need the object
            "sessionStudent": self.sessionStudent_id if self.sessionStudent else None,  # Or self.sessionStudent
            "questionIndex": self.questionIndex,
            "selectedOptions": self.selectedOptions,
            "userContext": self.userContext,
            "creationDate": timezone.localtime(self.creationDate).isoformat(),  # ISO format for datetimes
            "elapsedTime": self.elapsedTime,
            "isCorrect": self.isCorrect,
            "id": self.id # Include the id
        }