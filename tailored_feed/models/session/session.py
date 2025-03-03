from django.db import models
from django.utils.timezone import now
from django.db.models import JSONField
from tailored_feed.models.assessment.assessment import Assessment

class Session(models.Model):
    class State(models.TextChoices):
        CREATED = 'created', 'Created'
        WAITING = 'waiting', 'Waiting'
        IN_PROCESS = 'in_process', 'In Process'
        FINISHED = 'finished', 'Finished'
    
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name="session_assessment")
    creationDate = models.DateTimeField(default=now, editable=False)
    name = models.CharField(max_length=80)
    state = models.CharField(max_length=20, choices=State.choices, default=State.CREATED,)
    enrolledStudents = models.IntegerField(default=0) # At the moment the session started
    approvedStudents = models.IntegerField(default=0)
    disapprovedStudents = models.IntegerField(default=0)
    finishedStudents = models.IntegerField(default=0)
    feedbackEnabled = models.BooleanField(default=True)
    startDate = models.DateTimeField(null=True, blank=True)
    approvalModelQuestionIndicesAssessed = JSONField(default=list)

    class Meta:
        unique_together = ('assessment', 'creationDate')
        ordering = ['creationDate']
