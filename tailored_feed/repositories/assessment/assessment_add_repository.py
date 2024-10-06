from tailored_feed.models.assessment.assessment import Assessment

class AssessmentAddRepository:

    def add(self, name, owner):
        assessment = Assessment(name=name, owner=owner)
        assessment.save()

        return assessment