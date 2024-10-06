from django.db import models
from django.utils.timezone import now
from tailored_feed.models.assessment.assessment import Assessment

class AssessmentSession(models.Model):
    class State(models.TextChoices):
        WAITING = 'waiting', 'Waiting'
        IN_PROCESS = 'in_process', 'In Process'
        FINISHED = 'finished', 'Finished'
    
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name="session_assessment")
    creationDate = models.DateTimeField(default=now, editable=False)
    name = models.CharField(max_length=80)
    state = models.CharField(max_length=20, choices=State.choices, default=State.WAITING,)

    class Meta:
        unique_together = ('assessment', 'creationDate')
        ordering = ['creationDate']

    def __str__(self):
        return f"Session {self.name} for {self.assessmentId.name}"
