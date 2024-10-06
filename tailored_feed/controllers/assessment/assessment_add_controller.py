from django.shortcuts import render, redirect
from django.contrib import messages
from tailored_feed.repositories.assessment.assessment_add_repository import AssessmentAddRepository
from tailored_feed.services.assessment.assessment_add_service import AssessmentAddService

assessment_add_service = AssessmentAddService(AssessmentAddRepository())

class AssessmentAddController:

    @staticmethod
    def add(request):
        if request.method == 'POST':
            name = request.POST.get('name')
            assessment_add_service.add_n_save(name=name, owner=request.user)
            messages.success(request, 'La evaluación se creó exitosamente')
        
        return redirect('assessment_dashboard')