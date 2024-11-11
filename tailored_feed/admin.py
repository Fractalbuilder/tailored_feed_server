from django.contrib import admin
from tailored_feed.models.user import User
from tailored_feed.models.assessment.assessment import Assessment
from tailored_feed.models.session.session import Session
from tailored_feed.models.assessment.assessment_question import AssessmentQuestion
from tailored_feed.models.session.session_answer import SessionAnswer

admin.site.register(User)
admin.site.register(Assessment)
admin.site.register(Session)
admin.site.register(AssessmentQuestion)
admin.site.register(SessionAnswer)