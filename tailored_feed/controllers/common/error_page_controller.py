from django.shortcuts import render

class ErrorPageController:

    @staticmethod
    def show_view(request):
        return render(request, 'common/error_page.html')