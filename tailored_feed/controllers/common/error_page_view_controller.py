from django.shortcuts import render
from django.contrib.auth.decorators import login_required

class ErrorPageViewController:

    @staticmethod
    @login_required
    def view(request):
        return render(request, 'common/error_page.html')