from rest_framework import serializers
from tailored_feed.models import Session

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['assessmentId', 'creationDate', 'name', 'state']
        read_only_fields = ['creationDate']
