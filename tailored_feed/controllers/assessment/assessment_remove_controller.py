from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from tailored_feed.repositories.assessment.assessment_remove_repository import AssessmentRemoveRepository
from tailored_feed.services.assessment.assessment_remove_service import AssessmentRemoveService

assessment_remove_service = AssessmentRemoveService(AssessmentRemoveRepository())

class AssessmentRemoveController:

    @staticmethod
    def remove(request, assessment_id):
        if request.method == 'DELETE':
            assessment_remove_service.remove_n_save(assessment_id=assessment_id)
            messages.success(request, 'La evaluación se eliminó exitosamente')
        
        #return redirect('assessment_dashboard')
        return JsonResponse({'message': 'Assessment deleted successfully'}, status=200)