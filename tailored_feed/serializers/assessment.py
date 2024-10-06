from rest_framework import serializers
from tailored_feed.models import Assessment

class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = ['id', 'name', 'owner', 'creationDate']
        read_only_fields = ['id', 'creationDate']

    owner = serializers.PrimaryKeyRelatedField(read_only=True)

