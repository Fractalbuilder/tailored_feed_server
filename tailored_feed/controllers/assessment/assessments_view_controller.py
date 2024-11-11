import inspect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from tailored_feed.services.common.log_manager import LogManager
from tailored_feed.repositories.assessment.assessment_get_repository import AssessmentGetRepository
from tailored_feed.services.assessment.assessment_get_service import AssessmentGetService

log_manager = LogManager()
assessment_get_service = AssessmentGetService(AssessmentGetRepository())

class AssessmentsViewController:

    @staticmethod
    @login_required
    def view(request):
        try:
            owner_id = request.user.id
            assessments = assessment_get_service.by_owner_id(owner_id)

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
