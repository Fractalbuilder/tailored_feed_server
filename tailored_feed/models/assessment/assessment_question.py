from django.db import models
from tailored_feed.models.assessment.assessment import Assessment

class AssessmentQuestion(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name="question_assessment")
    statement = models.CharField(max_length=255)
    options = models.JSONField()
    feedback_text = models.TextField(blank=True, null=True)
    feedback_image = models.ImageField(upload_to='feedback_images/', blank=True, null=True)

    def __str__(self):
        return f"Question {self.statement} for assessment {self.assessment.name}"

    def to_dict(self):
        return {
            'id': self.id,
            'assessment': {
                'id': self.assessment.id,
                'name': self.assessment.name,
            },
            'statement': self.statement,
            'options': self.options,
            'feedback_text': self.feedback_text,
            'feedback_image': self.feedback_image.url if self.feedback_image else None
        }