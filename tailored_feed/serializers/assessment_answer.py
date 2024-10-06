from rest_framework import serializers
from tailored_feed.models import AssessmentAnswer

class AssessmentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentAnswer
        fields = ['id', 'assessmentSession', 'student', 'answer', 'creationDate']
        read_only_fields = ['creationDate']
