from rest_framework import serializers
from tailored_feed.models import AssessmentQuestion

class AssessmentQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentQuestion
        fields = ['id', 'assessment', 'title', 'question', 'feedback_text', 'feedback_image']
