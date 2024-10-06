from tailored_feed.models.assessment.assessment import Assessment

class AssessmentGetRepository:
    
    def all(self):
        return Assessment.objects.all().order_by('-creationDate')