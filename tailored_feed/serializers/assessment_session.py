from rest_framework import serializers
from tailored_feed.models import AssessmentSession

class AssessmentSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentSession
        fields = ['assessmentId', 'creationDate', 'name', 'state']
        read_only_fields = ['creationDate']
