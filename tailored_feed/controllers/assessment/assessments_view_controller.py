import inspect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from tailored_feed.services.common.log_manager import LogManager
from tailored_feed.repositories.assessment.assessment_get_repository import AssessmentGetRepository
from tailored_feed.services.assessment.assessment_get_service import AssessmentGetService

log_manager = LogManager()
assessment_get_service = AssessmentGetService(AssessmentGetRepository())

#from tailored_feed.services.ai.approval_sample_add_service import ApprovalSampleAddService
#approval_sample_add_service = ApprovalSampleAddService()

class AssessmentsViewController:

    @staticmethod
    @login_required
    def view(request):
        try:
            owner_id = request.user.id
            assessments = assessment_get_service.by_owner_id(owner_id)

            # Models test
            assessment_id = 19
            session_id = 100
            iteration = 0
            
            #approval_sample_add_service.train_model(assessment_id, session_id, iteration)

            # Pass
            student_data_pass = {
                'bandwidth': 32,
                'luminosity': 34,
                'noiseLevel': -35,
                'correctAnswers': 7,
                'elapsedTime': 16
            }
            
            # Fail
            student_data_fails = {
                'bandwidth': 20,
                'luminosity': 10,
                'noiseLevel': -10,
                'correctAnswers': 4,
                'elapsedTime': 20
            }

            #print("**** PREDICTION ****")       THIS IS DEPRECATED, IT WILL FAIL
            #print(approval_sample_add_service.predict_student_approval(student_data_pass, session_id, iteration))
            #print(approval_sample_add_service.predict_student_approval(student_data_fails, session_id, iteration))

            return render(
                request, 
                'assessment/assessments_view.html', 
                {'assessments': assessments}
            )

        except Exception as e:
            method_name = f"{__name__}.{inspect.currentframe().f_code.co_name}"
            sig = inspect.signature(AssessmentsViewController.view)
            param_names = [p.name for p in sig.parameters.values() if p.kind == p.POSITIONAL_OR_KEYWORD]
            parameters = {k: v for k, v in locals().items() if k in param_names and k != 'self'}
            log_manager.log_report(method_name, parameters, str(e))

            return redirect('error_page')
