from django.db import models
from tailored_feed.models.assessment.assessment import Assessment

class ApprovalSample(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name="approval_sample_assessment")
    iteration = models.IntegerField(default=-1)
    isPredicted = models.BooleanField(default=False)
    isApproved = models.BooleanField(default=False)
    bandwidth = models.FloatField()
    luminosity = models.FloatField()
    noiseLevel = models.FloatField()
    correctAnswers = models.IntegerField()
    elapsedTime = models.FloatField()

    def to_dict(self):

        return {
            'id': self.id,
            "assessment": self.assessment_id if self.assessment else None, 
            'iteration': self.iteration,
            'isPredicted': self.isPredicted,
            'isApproved': self.isApproved,
            'bandwidth': self.bandwidth,
            'luminosity': self.luminosity,
            'noiseLevel': self.noiseLevel,
            'correctAnswers': self.correctAnswers,
            'elapsedTime': self.elapsedTime
        }