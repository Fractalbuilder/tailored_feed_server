from django.shortcuts import render

class ErrorPageViewController:

    @staticmethod
    def view(request):
        return render(request, 'common/error_page.html')