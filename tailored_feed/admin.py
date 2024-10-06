from django.contrib import admin
from tailored_feed.models.user import User
from tailored_feed.models.assessment.assessment import Assessment
from tailored_feed.models.assessment.assessment_session import AssessmentSession
from tailored_feed.models.assessment.assessment_question import AssessmentQuestion
from tailored_feed.models.assessment.assessment_answer import AssessmentAnswer

admin.site.register(User)
admin.site.register(Assessment)
admin.site.register(AssessmentSession)
admin.site.register(AssessmentQuestion)
admin.site.register(AssessmentAnswer)