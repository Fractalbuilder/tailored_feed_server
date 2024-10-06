from django.shortcuts import render, redirect
from tailored_feed.repositories.assessment.assessment_get_repository import AssessmentGetRepository
from tailored_feed.services.assessment.assessment_get_service import AssessmentGetService

assessment_get_service = AssessmentGetService(AssessmentGetRepository())

class AssessmentDashboardController:

    @staticmethod
    def show_view(request):
        assessments = []
        assessments = assessment_get_service.all()

        return render(
            request, 
            'assessment/assessment_dashboard.html', 
            {'assessments': assessments}
        )