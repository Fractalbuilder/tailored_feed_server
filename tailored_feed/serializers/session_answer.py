from rest_framework import serializers
from tailored_feed.models.session.session_answer import SessionAnswer

class SessionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionAnswer
        fields = ['id', 'assessment_question', 'session_student', 'optionanswered', 'creationDate']
        read_only_fields = ['creationDate']
