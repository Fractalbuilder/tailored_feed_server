import inspect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from tailored_feed.services.common.log_manager import LogManager
from tailored_feed.forms.authentication_form import LoginForm

log_manager = LogManager()

class AuthenticationViewController():
    
    @staticmethod
    def login_view(request):
        try:
            if request.method == 'POST':
                form = LoginForm(request.POST)

                if form.is_valid():
                    username = form.cleaned_data['username']
                    password = form.cleaned_data['password']
                    user = authenticate(request, username=username, password=password)

                    if user is not None:
                        login(request, user)

                        if user.role == 'teacher':
                            return redirect('assessments_view')
                        else:
                            messages.error(request, "Usted no cuenta con permisos")
                    else:
                        messages.error(request, "Usuario o clave inválido")
            else:
                form = LoginForm()

            return render(request, 'authentication/login.html', {'form': form})

        except Exception as e:
            method_name = f"{__name__}.{inspect.currentframe().f_code.co_name}"
            sig = inspect.signature(AuthenticationViewController.login_view)
            param_names = [p.name for p in sig.parameters.values() if p.kind == p.POSITIONAL_OR_KEYWORD]
            parameters = {k: v for k, v in locals().items() if k in param_names and k != 'self'}
            log_manager.log_report(method_name, parameters, str(e))

            return redirect('error_page')

    @staticmethod
    def logout(request):
        logout(request)
        response = redirect('login')
        response.delete_cookie('sessionid')
        return response
