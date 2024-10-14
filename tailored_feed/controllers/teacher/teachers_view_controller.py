from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def teachers_view(request):
    return render(request, 'teacher/teachers_view.html')
