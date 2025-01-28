from django.shortcuts import render
from django.http import StreamingHttpResponse
import json
import time
from tailored_feed.repositories.session.session_get_repository import SessionGetRepository
from tailored_feed.services.session.session_get_service import SessionGetService

session_get_service = SessionGetService(SessionGetRepository())

def index(request):
    return render(request, "common/index.html")


def sse_sessions(request):
    def event_stream():
        print("New connection")
        counter = 0
        
        while True:
            sessions = session_get_service.all_active()
            sessions_data = [
                {"id": session.id, "name": session.name, "totalQuestions": session.assessment.totalQuestions}
                for session in sessions
            ]

            yield f"data: {json.dumps(sessions_data)}\n\n"
            time.sleep(2)
            print(counter)
            counter += 1

    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    return response
