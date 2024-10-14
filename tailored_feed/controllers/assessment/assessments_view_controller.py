import inspect
from django.shortcuts import render, redirect
from tailored_feed.services.common.log_manager import LogManager
from tailored_feed.repositories.assessment.assessment_get_repository import AssessmentGetRepository
from tailored_feed.services.assessment.assessment_get_service import AssessmentGetService

log_manager = LogManager()
assessment_get_service = AssessmentGetService(AssessmentGetRepository())

class AssessmentsViewController:

    @staticmethod
    def view(request):
        try:
            assessments = assessment_get_service.all()

            return render(
                request, 
                'assessment/assessments_view.html', 
                {'assessments': assessments}
            )

        except Exception as e:
            nombre_metodo = f"{__name__}.{inspect.currentframe().f_code.co_name}"
            argspec = inspect.getfullargspec(lambda: view())
            parametros = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            log_manager.log_report(nombre_metodo, parametros, str(e))

            return redirect('error_page')