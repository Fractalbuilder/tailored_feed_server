from tailored_feed.models.assessment.assessment import Assessment

class AssessmentRemoveRepository:

    def remove(self, assessment_id: int):
        assessment = Assessment.objects.get(id=assessment_id)
        assessment.delete()