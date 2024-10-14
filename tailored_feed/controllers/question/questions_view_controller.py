import inspect
from django.shortcuts import render, redirect
from tailored_feed.services.common.log_manager import LogManager
from tailored_feed.repositories.assessment.assessment_get_repository import AssessmentGetRepository
from tailored_feed.repositories.question.question_get_repository import QuestionGetRepository
from tailored_feed.services.assessment.assessment_get_service import AssessmentGetService
from tailored_feed.services.question.question_get_service import QuestionGetService

log_manager = LogManager()
assessment_get_service = AssessmentGetService(AssessmentGetRepository())
question_get_service = QuestionGetService(QuestionGetRepository())

class QuestionsViewController:

    @staticmethod
    def view(request, assessment_id):
        try:
            assessment = assessment_get_service.by_id(assessment_id)
            assessment_editable = assessment.editable
            questions = question_get_service.by_assessment_id(assessment_id)
            context = {
                'assessment': {
                    'id': assessment_id,
                    'editable': assessment_editable
                }
            }

            return render(
                request, 
                'question/questions_view.html', 
                {'context': context, 'questions': questions}
            )
            
        except Exception as e:
            nombre_metodo = f"{__name__}.{inspect.currentframe().f_code.co_name}"
            argspec = inspect.getfullargspec(lambda: view())
            parametros = {name: value for name, value in locals().copy().items() if name in argspec.args and name != 'self'}
            log_manager.log_report(nombre_metodo, parametros, str(e))

            return redirect('error_page')
