from django.db import models
from tailored_feed.models.assessment.assessment import Assessment

class AssessmentQuestion(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name="question_assessment")
    title = models.CharField(max_length=255)
    question = models.JSONField()
    feedback_text = models.TextField(blank=True, null=True)
    feedback_image = models.ImageField(upload_to='feedback_images/', blank=True, null=True)

    def __str__(self):
        return f"Question {self.title} for assessment {self.assessment.name}"
