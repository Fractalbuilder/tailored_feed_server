from django.db import models
from django.utils.timezone import now
from tailored_feed.models.session.session import Session
from tailored_feed.models.user import User

class SessionStudent(models.Model):    
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="session_student_ses")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="session_student_stu")
    creationDate = models.DateTimeField(default=now, editable=False)

    class Meta:
        unique_together = ('session', 'student')
        ordering = ['creationDate']