from django.db import models
from django.utils.timezone import now
from tailored_feed.models.session.session import Session
from tailored_feed.models.user import User

class SessionStudent(models.Model):
    
    class ApprovalPrediction(models.TextChoices):
        NOT_PREDICTED = 'not_predicted'
        APPROVED = 'approved'
        DISAPPROVED = 'disapproved'
    
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="session_student_ses")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="session_student_stu")
    creationDate = models.DateTimeField(default=now, editable=False)
    correctAnswers = models.IntegerField(default=0)
    wrongAnswers = models.IntegerField(default=0)
    currentQuestionIndex = models.IntegerField()
    grade = models.FloatField(blank=True, null=True)
    approvalPrediction = models.CharField(max_length=20, choices=ApprovalPrediction.choices, default=ApprovalPrediction.NOT_PREDICTED,)

    class Meta:
        unique_together = ('session', 'student')
        ordering = ['creationDate']