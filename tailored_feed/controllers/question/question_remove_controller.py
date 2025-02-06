import inspect
from django.shortcuts import redirect
from django.contrib import messages
from tailored_feed.exceptions.content_error import ContentError
from tailored_feed.services.common.log_manager import LogManager
from django.contrib.auth.decorators import login_required
from tailored_feed.repositories.assessment.assessment_add_repository import AssessmentAddRepository
from tailored_feed.repositories.assessment.assessment_get_repository import AssessmentGetRepository
from tailored_feed.repositories.question.question_remove_repository import QuestionRemoveRepository
from tailored_feed.services.assessment.assessment_add_service import AssessmentAddService
from tailored_feed.services.assessment.assessment_get_service import AssessmentGetService
from tailored_feed.services.question.question_remove_service import QuestionRemoveService

log_manager = LogManager()
assessment_add_service = AssessmentAddService(AssessmentAddRepository())
assessment_get_service = AssessmentGetService(AssessmentGetRepository())
question_remove_service = QuestionRemoveService(QuestionRemoveRepository(), assessment_add_service)

class QuestionRemoveController:

    @staticmethod
    @login_required
    def remove(request):
        try:
            if request.method != 'POST':
                raise ContentError('La petición no usa el método POST')
            
            id = request.POST.get('id')
            assessment_id = request.POST.get('assessment_id')
            assessment = assessment_get_service.by_id(assessment_id)
            question_remove_service.remove_n_save(id=id, assessment=assessment)
            messages.success(request, 'La pregunta se eliminó exitosamente')

        except ContentError as e:
            messages.error(request, "Eliminación fallida. " + str(e))

        except Exception as e:
            method_name = f"{__name__}.{inspect.currentframe().f_code.co_name}"
            sig = inspect.signature(QuestionRemoveController.remove)
            param_names = [p.name for p in sig.parameters.values() if p.kind == p.POSITIONAL_OR_KEYWORD]
            parameters = {k: v for k, v in locals().items() if k in param_names and k != 'self'}
            log_manager.log_report(method_name, parameters, str(e))

            return redirect('error_page')

        return redirect('questions_view', assessment_id=assessment_id)